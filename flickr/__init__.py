from collections import defaultdict
from settings import FLICKR_API_SECRET, FLICKR_API_KEY
import flickrapi
from PIL import Image
from xml.etree import ElementTree
from lxml import objectify
import requests
from io import StringIO

CLIENT = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, cache=True)

def mkobjectify(tree):
    return objectify.fromstring(ElementTree.tostring(tree))

def get_average_color(url):
    resp = requests.get(url)
    if resp.ok:
        i = Image.open(StringIO(resp.content))
        h = i.histogram()
        r = h[0:256]
        g = h[256:256*2]
        b = h[256*2: 256*3]

        return (
            sum( i*w for i, w in enumerate(r) ) / sum(r),
            sum( i*w for i, w in enumerate(g) ) / sum(g),
            sum( i*w for i, w in enumerate(b) ) / sum(b)
        )

def sizes_from_id(photo_id):
    resp = CLIENT.photos_getSizes(photo_id=photo_id)
    if len(resp):
        elems = resp.getchildren()[0]
        attrib_list = [a.attrib for a in elems]
        ret = {}
        for size in attrib_list:
            ret[size.pop('label')] = size
        return ret

def image_info(photo_id):

    resp = mkobjectify(CLIENT.photos_getInfo(photo_id=photo_id))
    sizes = sizes_from_id(photo_id)
    # workout average color from small image
    average_color = get_average_color(sizes.get('Small',{}).get('source'))

    ret =  {
        'title': str(resp.photo.title),
        'tags': [str(x.text).encode('utf-8') for x in resp.photo.tags.getchildren()],
        'sizes': sizes,
        'bgcolor': 'rgb({},{},{})'.format(*average_color)
    }
    return ret

