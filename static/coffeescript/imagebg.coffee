#console.log 'image lib loaded'
__pckl = __pckl || {}
((root, $) ->
  root.Photo = root.Photo || {}

  root.Nav = root.Nav || {}


  goto_url = (url) ->
    window.location = url

    
  root.Nav.init = () ->
    if 'prev' of root.Nav and 'next' of root.Nav
        $('body').keydown (evt) ->
          console.log evt.which
          switch (evt.which)
            when 39, 76
              goto_url root.Nav.next
            when 37, 72
              goto_url root.Nav.prev
    null
  
  sizes =
    75: 'square-src'
    150: 'large-square-src'
    100: 'thumbnail-src'
    240: 'small-src'
    320: 'small320-src'
    500: 'medium-src'
    640: 'medium640-src'
    800: 'medium800-src'
    1024: 'large-src'
    1600: 'large1600-src'
    2048: 'large2048-src'

  root.Photo.init = (config) ->
    viewport_w = $(window).width() * (window.devicePixelRatio || 1)
    required_size = undefined
    for wsz, klass of sizes
      if wsz > viewport_w
        required_size = klass
        break
    if not required_size
      required_size = 'original'
    img = $('div#img')
    article = $('article.photo')
    url = img.data(required_size) 
    article.css('background', "url(#{url}) no-repeat center center fixed")
    article.css('-webkit-background-size', 'contain')
    article.css('-moz-background-size', 'contain')
    article.css('-o-background-size', 'contain')
    article.css('-ms-background-size', 'contain')
    article.css('background-size', 'contain')
    article.data('using', required_size)
  root
) __pckl, jQuery
