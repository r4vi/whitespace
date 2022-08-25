import argparse
import datetime
import re
import os
import yaml
import unicodedata
#import flickr
import dateutil.parser


def mkdate(d):
    return dateutil.parser.parse(d)


parser = argparse.ArgumentParser()
parser.add_argument_group()
parser.add_argument('-n', '--new')
parser.add_argument('-t', '--title')
parser.add_argument('-d', '--date', type=mkdate)
# parser.add_argument('-p', '--photo')


CONTENT_PATH = os.path.join(os.path.dirname(__file__), '../content/')


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower()).strip()
    return re.sub(r'[-\s]+', '-', value)


def new_generic(content_type):

    def _f(name, date=None):
        CONTENT_TYPE = content_type
        title = name
        name = slugify(name)
        path = os.path.abspath(os.path.join(
            CONTENT_PATH, CONTENT_TYPE, name + '.md'))
        if os.path.isfile(path):
            # bail out
            raise ValueError("File with name {} already exists".format(name))
        if not date:
            date = datetime.datetime.now()
        preamble = {
            'title': title,
            'date': date
        }
        dump = '---\n'
        dump += yaml.dump(
            preamble,
            default_flow_style=False
        )
        dump += '---\n\n'

        with open(path, 'w') as f:
            f.write(dump)
    return _f


new_milestone = new_generic('milestone')
new_post = new_generic('post')
new_short = new_generic('short')


def handle_command(*args):
    args = parser.parse_args()
    if args.new:
        if args.new.startswith('milestone'):
            new_milestone(args.title, date=args.date)
        elif args.new.startswith('post'):
            new_post(args.title, date=args.date)
        elif args.new.startswith('short'):
            new_short(args.title, date=args.date)
    print(args)
