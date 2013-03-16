from settings import FLICKR_API_SECRET, FLICKR_API_KEY
import flickrapi
CLIENT = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, cache=True)

def sizes_from_id(photo_id):
    resp = CLIENT.photos_getSizes(photo_id=photo_id)
    if len(resp):
        elems = resp.getchildren()[0]
        attrib_list = [a.attrib for a in elems]
        ret = {}
        for size in attrib_list:
            ret[size.pop('label')] = size
        return ret