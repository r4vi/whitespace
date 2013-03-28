date: 2011-11-22 00:00:00
title: Javascript Page Reload with Cross Browser Compatibility

```javascript
    var meta;
    if (document.createElement && (meta = document.createElement('meta')) {
    meta.httpEquiv = 'refresh';
    meta.content = '1;'
    document.getElementsByTagName('head').item(0).appendChild(meta);
    }
```