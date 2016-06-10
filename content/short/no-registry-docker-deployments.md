date: 2016-06-10 21:06:34.830696
title: No Registry Docker Deployments
tags:
    - docker
    - devops
    - linux
    
Sometimes you want to deploy an application that's packaged as a Docker
container but you don't want to set up a registry.  Not that setting one 
up is hard with [AWS ECR][awsecr] or Google Cloud's
[containter registry][gcmreg] but this approach is _really_ simple 
and doesn't add
any complexity to your infrastructure.

### The problem

I had a situation where I already had a batch job that was orchestrated to run
nightly and I wanted to run an application during that batch but:

* I didn't want to install anything on that server
* I wanted to be able to deploy new versions of the dockerised application
  separately from the batch job.

It's not important what the batch job does but here's a quick overview
for flavor. It gets a very large XML file and
spits out a directory of thousands of `.json` files for each element in the XML.
I needed to index all of these files in [Elasticsearch][es].

So here's how I did it using a Makefile and S3

####  Building

Imagine this `Makefile` is at the root of a working Docker project.

When you type `make` on the command line it will:

* Build the image and tag it `elasticsearch-index`
* Export the image to a file called `elasticsearch-index.tar.xz` using `docker
  save` which is around 20MB in size ([alpine][alpine] based image)
* Upload the image to Amazon S3 both as a filename based on the SHA256 of the
  content of `elasticsearch-index.tar.xz` and as
  `elasticsearch-index-latest.tar.xz` for convenience

```make
.PHONY: build_docker_tar push_to_s3 default docker_image

NAME := elasticsearch-index
SHELL := /bin/bash
SHA=$(shell openssl sha256 -r elasticsearch-index.tar.xz | cut -d" " -f1)

default: push_to_s3

docker_image:    .
    docker build -t $(NAME) .
    @docker inspect -f '{{.Id}}' $(NAME) > .built

clean:
    @rm .built

elasticsearch-index.tar.xz: docker_image
    docker save elasticsearch-index | xz > elasticsearch-index.tar.xz

build_docker_tar: elasticsearch-index.tar.xz

push_to_s3: build_docker_tar
    aws s3api head-bucket --bucket docker-elasticsearch-index || aws s3 mb s3://docker-elasticsearch-index || true
    aws s3 cp ./elasticsearch-index.tar.xz s3://docker-elasticsearch-index/$(SHA).tar.xz
    aws s3 cp s3://docker-elasticsearch-index/$(SHA).tar.xz s3://docker-elasticsearch-index/elasticsearch-index-latest.tar.xz
```

####  Running

The server running the batch job is an AWS EC2 instance so I configured it to
launch with an [Instance Profile][instp] so that it transparently has access to S3
without me manually having to change anything on that server.

Here is a excerpt of the bash script that runs the batch:

```bash
function es_import_docker() {
  aws s3 cp $ES_INDEXER_DOCKER_IMAGE /tmp/es-infra.tar.xz
  xzcat /tmp/es-infra.tar.xz | sudo docker load
  sudo docker images
  sudo docker ps
}

function es_index() {
  OUTPUT_DIR=$1
  es_import_docker
  docker run --rm --name indexer -v $OUTPUT_DIR:/usr/src/data:ro elasticsearch-index python index.py $ENVIRONMENT_NAME

}
```

Basically there is a function in that batch job that calls `es_index` with a
parameter being the path to the JSON files that need to be indexed into
Elasticsearch.

💥

#### Conclusion

This has been running for over 6 months in production and we've never had it
fail and at the same time we've been able to develop and test new revisions,
spin up a new environment for the batch job, point it at the new container and
test that it works. 

This workflow has been extremely convenient, cheap and has
the availability of S3. 

If this offends you greatly or you think I'm doing it wrong then let me know on
[twitter][twitter].


[awsecr]: https://aws.amazon.com/ecr/
[gcmreg]: https://cloud.google.com/container-registry/
[instp]: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html
[twitter]: https://twitter.com/r4vi
[es]: https://www.elastic.co/
[alpine]: http://www.alpinelinux.org/
