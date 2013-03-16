from operator import itemgetter
import sys, os
from commands import handle_command
from flask import Flask, render_template, send_from_directory
from flask_flatpages import FlatPages
import flickr
import markdown2
from flask_frozen import Freezer
from jinja2.exceptions import TemplateNotFound
from flaskext.compass import Compass
import flask_assets
from settings import FLICKR_API_KEY, FLICKR_API_SECRET
from webassets import Bundle


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = './content/'
FLATPAGES_HTML_RENDERER = lambda x: markdown2.markdown(x, extras=["footnotes", 
                                                "fenced-code-blocks",
                                                "header-ids",
                                                "smarty-pants"])
SITE_NAME = 'Ravi - Pickled Lime'


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

@app.route('/')
def index():
    milestones = MODELS.get('milestones')
    return render_template('homepage.jade', title='Ravi Kotecha', milestones=milestones)


@app.route('/short/')
def short_index():
    shorts = MODELS.get('shorts')
    return render_template('short_index.jade', shorts=shorts, title='Shorts')

@app.route('/post/')
def post_index():
    posts = MODELS.get('posts')
    return render_template('post_index.jade', posts=posts, title='Posts')

@app.route('/photo/')
def photo_index():
    photos = MODELS.get('photos')

    return render_template('photo_index.jade', photos=photos, title='Photos')

@app.route('/photo/<path:path>/')
def photo_entry(path):
    full_path = 'photo/' + path
    page = pages.get_or_404(full_path)
    sizes = flickr.sizes_from_id(page.meta.get('photo_id'))

    return render_template('photo.jade', page=page, sizes=sizes, title=page.meta.get('title', 'Untitled'))

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

@freezer.register_generator
def page():
    for p in pages:
        yield {'path': p.path}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            freezer.freeze()
        else:
            handle_command(sys.argv[1:])
            #handle creating new photos here
    else:
        app.run(port=9090, debug=DEBUG)
