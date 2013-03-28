from StringIO import StringIO
from fabric.api import *
from fabric.contrib.files import exists
from fabric.operations import get, put
from fabric.contrib.project import rsync_project
from cStringIO import StringIO
import os


from jinja2 import Template, Environment, FileSystemLoader

jinja_env = Environment(loader=FileSystemLoader('templates'))

env.user = 'ravi'
env.hosts =['pckl.me']
VHOST  = 'ravi.pckl.me'
APP_DIR = '/var/www/%s/' % VHOST
NGINX_DIR = '/etc/nginx/sites-'



def _make_vhost():
    template = jinja_env.get_template('nginx.conf.jinja2')
    interpolated = StringIO()
    interpolated.write(template.render({
        'domain': VHOST,
        'root': APP_DIR,
    }))
    put(interpolated, '%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST}, use_sudo=True)
    if not exists('%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST}):
        sudo('ln -s %(src)s %(tar)s' % {'src': '%(nginx)savailable/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST},
                                    'tar': '%(nginx)senabled/%(vhost)s' % {'nginx': NGINX_DIR, 'vhost': VHOST}}
    )

    run('touch %s/log/access.log' % APP_DIR)
    run('touch %s/log/error.log' % APP_DIR)
    sudo('service nginx configtest')
    sudo('service nginx reload')

def build():
    local('venv/bin/python sitebuilder.py build')

def deploy():
    rsync_project('/var/www/ravi.pckl.me/public/', local_dir='build/',
    exclude=[
        'static/.sass-cache/',
        'static/.webassets-cache/'
    ])

def bootstrap():
    run('mkdir -p {0}'.format(APP_DIR))
    run('mkdir -p {0}'.format(os.path.join(APP_DIR,'log')))
    run('mkdir -p {0}'.format(os.path.join(APP_DIR,'backup')))
    run('mkdir -p {0}'.format(os.path.join(APP_DIR,'private')))
    run('mkdir -p {0}'.format(os.path.join(APP_DIR,'public')))
    _make_vhost()

