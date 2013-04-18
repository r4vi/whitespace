from collections import defaultdict
from operator import itemgetter
import sys, os
import itertools
from urlparse import urljoin
import datetime
from commands import handle_command
from flask import Flask, render_template, send_from_directory, request
from flask_flatpages import FlatPages
import flickr
import markdown2
from flask_frozen import Freezer
from jinja2.exceptions import TemplateNotFound
from flaskext.compass import Compass
import flask_assets
from settings import FLICKR_API_KEY, FLICKR_API_SECRET
from webassets import Bundle
from werkzeug.contrib.atom import AtomFeed

DEBUG = True
if len(sys.argv) > 1:
    if sys.argv[1] == "build":
        DEBUG = False

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = './content/'
FLATPAGES_HTML_RENDERER = lambda x: markdown2.markdown(x, extras=["footnotes", 
                                                "fenced-code-blocks",
                                                "header-ids",
                                                "smarty-pants"])
SITE_NAME = 'Ravi - Pickled Lime'
SITE_ROOT = 'http://ravi.pckl.me'

app = Flask(__name__)
app.config.from_object(__name__)

app.config['ASSETS_DEBUG'] = DEBUG
assets = flask_assets.Environment(app)
assets.init_app(app)
assets.debug = DEBUG

app.jinja_env.add_extension('webassets.ext.jinja2.AssetsExtension')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
pages = FlatPages(app)
freezer = Freezer(app)
compass = Compass(app)

common_js = Bundle('js/modernizr.custom.59903.js', 'js/jquery-1.9.1.min.js', output='js/gen/common.js', filters='rjsmin')
photo_js = Bundle('coffeescript/imagebg.coffee', output='js/gen/imagebg.js', filters='coffeescript,rjsmin')
assets.register('photo_js', photo_js)
assets.register('common_js', common_js)

MODELS = {
    'shorts': sorted([p for p in pages if p.path.startswith('short/')], key=lambda x: x.meta.get('date'), reverse=True),
    'posts': sorted([p for p in pages if p.path.startswith('post/')], key=lambda x: x.meta.get('date'), reverse=True),
    'photos': sorted([p for p in pages if p.path.startswith('photo/')], key=lambda x: x.meta.get('date'), reverse=True),
    'milestones': sorted([p for p in pages if p.path.startswith('milestone/')], key=lambda x: x.meta.get('date'), reverse=True),
}
MODELS['all'] = sorted(itertools.chain.from_iterable(MODELS.values()), key=lambda x: x.meta.get('date'), reverse=True)

@app.before_request
def before_req():
    if DEBUG:
        global MODELS
        # in debug mode, refresh models on every request
        MODELS = {
            'shorts': sorted([p for p in pages if p.path.startswith('short/')], key=lambda x: x.meta.get('date'), reverse=True),
            'posts': sorted([p for p in pages if p.path.startswith('post/')], key=lambda x: x.meta.get('date'), reverse=True),
            'photos': sorted([p for p in pages if p.path.startswith('photo/')], key=lambda x: x.meta.get('date'), reverse=True),
            'milestones': sorted([p for p in pages if p.path.startswith('milestone/')], key=lambda x: x.meta.get('date'), reverse=True),
            }
        MODELS['all'] = sorted(itertools.chain.from_iterable(MODELS.values()), key=lambda x: x.meta.get('date'), reverse=True)

def make_external(url):
    return urljoin(SITE_ROOT, url)


@app.route('/')
def index():
    milestones = MODELS.get('milestones')
    return render_template('homepage.jade', title='Ravi Kotecha', milestones=milestones)


@app.route('/feed.atom')
def recent_feed():
    feed = AtomFeed('Ravi Kotecha - Recent Posts',
                    feed_url=urljoin(SITE_ROOT, 'feed.atom'),
                    url=SITE_ROOT)
    posts = MODELS.get('all')[:25]
    for post in posts:

        feed.add(post.meta.get('title', 'untitled'),
                 post.html,
                 content_type='html',
                 author='Ravi Kotecha',
                 url=make_external(post.path),
                 updated=post.meta.get('date', datetime.datetime.now())
        )
    return feed.get_response()

@app.route('/short/')
def short_index():
    shorts = MODELS.get('shorts')
    return render_template('short_index.jade', shorts=shorts, title='Shorts')

@app.route('/post/')
def post_index():
    posts = [p for p in MODELS.get('posts') if 'draft' not in p.meta.get('tags', [])]
    return render_template('post_index.jade', posts=posts, title='Posts')

@app.route('/photo/')
def photo_index():
    photos = MODELS.get('photos')

    return render_template('photo_index.jade', photos=photos, title='Photos')

def _to_default_dict(d):
    orig = d.get('Original')
    ret = defaultdict(lambda: orig)
    ret.update(d)
    return ret

@app.route('/photo/<path:path>/')
def photo_entry(path):
    full_path = 'photo/' + path
    page = pages.get_or_404(full_path)

    sizes = _to_default_dict(page.meta.get('sizes')) or flickr.sizes_from_id(page.meta.get('photo_id'))

    return render_template('photo.jade', page=page,
        sizes=sizes,
        title=page.meta.get('title', 'Untitled'),
        bgcolor=page.meta.get('bgcolor')
    )

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = 'flatpage.jade'
    try:
        guess_template = path.split('/')[0] + '.jade'
        app.jinja_env.get_template(guess_template)
        # todo, allow overriding in markdown
        template = guess_template
    except TemplateNotFound:
        pass
    return render_template(template, page=page, title=page.meta.get('title', 'Untitled'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
      os.path.join(
        app.root_path, 'static', 'images'), 
      'favicon.ico', 
      mimetype='image/vnd.microsoft.icon') 

@app.route('/robots.txt')
def robots():
    return send_from_directory(
      os.path.join(
        app.root_path, 'static'), 
      'robots.txt', 
      mimetype='text/plain') 

@freezer.register_generator
def page():
    for p in pages:
        yield {'path': p.path}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            DEBUG = False
            freezer.freeze()
        else:
            handle_command(sys.argv[1:])
            #handle creating new photos here
    else:
        app.run(port=9090, debug=DEBUG)
