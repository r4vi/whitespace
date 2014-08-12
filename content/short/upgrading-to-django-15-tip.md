date: 2013-04-11 19:10:44.199356
title: 'Upgrading to Django 1.5 Tip'

If you're upgraging to Django 1.5 and have old format `{% url blah %}`
links in your templates it can be quite painful to convert to the new
format ```{% url 'blah' %}``` manually. 

Here's a regex you can use to convert all of your templates in one go:

Find: ```(\{%\surl\s)([^"|'\\][^\s]*)(?:[^"|'\\])*?```

Replace: ```$1 '$2'```
