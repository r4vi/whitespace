#!/bin/bash


aws s3 sync --cache-control max-age=900 ./build/ s3://ravi.pckl.me/ --acl=public-read --region us-east-1 --exclude=static/.*-cache/* --delete
