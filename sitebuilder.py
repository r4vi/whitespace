import sys, os
from flask import Flask, render_template
from flask_flatpages import FlatPages
import markdown2
from flask_frozen import Freezer
from jinja2.exceptions import TemplateNotFound
from flaskext.compass import Compass


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = './content/'
FLATPAGES_HTML_RENDERER = lambda x: markdown2.markdown(x, extras=["footnotes", 
                                                "fenced-code-blocks",
                                                "header-ids",
                                                "smarty-pants"])



app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


pages = FlatPages(app)
freezer = Freezer(app)
compass = Compass(app)

@app.route('/')
def index():
    return "hello turds"

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


    return render_template(template, page=page)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=9090, debug=DEBUG)
