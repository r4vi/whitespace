var __pckl;

__pckl = __pckl || {};

(function(root, $) {
  var goto_url, sizes;
  root.Photo = root.Photo || {};
  root.Nav = root.Nav || {};
  goto_url = function(url) {
    return window.location = url;
  };
  root.Nav.init = function() {
    if ('prev' in root.Nav && 'next' in root.Nav) {
      $('body').keydown(function(evt) {
        console.log(evt.which);
        switch (evt.which) {
          case 39:
          case 76:
            return goto_url(root.Nav.next);
          case 37:
          case 72:
            return goto_url(root.Nav.prev);
        }
      });
    }
    return null;
  };
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
    var article, img, klass, required_size, url, viewport_w, wsz;
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
    img = $('div#img');
    article = $('article.photo');
    url = img.data(required_size);
    article.css('background', "url(" + url + ") no-repeat center center fixed");
    article.css('-webkit-background-size', 'contain');
    article.css('-moz-background-size', 'contain');
    article.css('-o-background-size', 'contain');
    article.css('-ms-background-size', 'contain');
    article.css('background-size', 'contain');
    return article.data('using', required_size);
  };
  return root;
})(__pckl, jQuery);
