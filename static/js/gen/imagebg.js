var __pckl;

__pckl = __pckl || {};

(function(root, $) {
  var sizes;
  root.Photo = {};
  sizes = {
    75: 'square-src',
    150: 'large-square-src',
    100: 'thumbnail-src',
    240: 'small-src',
    320: 'small320-src',
    500: 'medium-src',
    640: 'medium640-src',
    800: 'medium800-src',
    1024: 'large-src',
    1600: 'large1600-src',
    2048: 'large2048-src'
  };
  root.Photo.init = function(config) {
    var img, klass, required_size, viewport_w, wsz;
    viewport_w = $(window).width() * (window.devicePixelRatio || 1);
    required_size = void 0;
    for (wsz in sizes) {
      klass = sizes[wsz];
      if (wsz > viewport_w) {
        required_size = klass;
        break;
      }
    }
    if (!required_size) {
      required_size = 'original';
    }
    img = $('img');
    img.attr('src', img.data(required_size));
    return img.data('using', required_size);
  };
  return root;
})(__pckl, jQuery);
