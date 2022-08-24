import argparse
import datetime
import os
import yaml
from unicodedata import normalize
import flickr
import dateutil.parser

def mkdate(d):
    return dateutil.parser.parse(d)

parser = argparse.ArgumentParser()
parser.add_argument_group()
parser.add_argument('-n','--new')
parser.add_argument('-t', '--title')
parser.add_argument('-d', '--date', type=mkdate)
parser.add_argument('-p', '--photo')


CONTENT_PATH = os.path.join(os.path.dirname(__file__), '../content/')



def slugify(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = [x if x in permitted_chars else '' for x in ascii_text]
    return ''.join(strict_text)


def new_photo(photo_id, date=None):
    CONTENT_TYPE = 'photo'
    info = flickr.image_info(photo_id)
    name = str(info.get('title', photo_id))
    slug = slugify(name)

    path = os.path.abspath(os.path.join(CONTENT_PATH, CONTENT_TYPE, slug + '.md'))
    if os.path.isfile(path):
        # bail out
        raise ValueError("File with name {} already exists".format(slug))
    if not date:
        date = datetime.datetime.now()

    preamble = {
        'title': name,
        'date': date,
        'photo_id': photo_id
    }
    info.update(preamble)
    preamble = info

    dump = yaml.dump(
        preamble,
        default_flow_style=False
    )
    dump += '\n'*2

    with open(path, 'wb') as f:
        f.write(dump)

def new_generic(content_type):

    def _f(name, date=None):
        CONTENT_TYPE = content_type
        title = name
        name = slugify(name)
        path = os.path.abspath(os.path.join(CONTENT_PATH, CONTENT_TYPE, name + '.md'))
        if os.path.isfile(path):
            # bail out
            raise ValueError("File with name {} already exists".format(name))
        if not date:
            date = datetime.datetime.now()
        preamble = {
            'title': title,
            'date': date
        }

        dump = yaml.dump(
            preamble,
            default_flow_style=False
        )
        dump += '\n'*2

        with open(path, 'wb') as f:
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
        elif args.new.startswith('photo'):
            new_photo(args.photo, date=args.date)
    print(args)