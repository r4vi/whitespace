date: 2014-10-04 11:04:49.622536
title: Copy and Paste Driven Development
tags:
    - programming
    - javascript
    - python
    - sql

*This post isn't a rant about copy and pasting code you don't understand into your projects.*
    
I was recently convinced by a college that declaring variables in ```javascript``` should be
done like this:

```javascript
var foo = '123';
var bar = '789';
var baz = '000';
```

Instead of the more often recommended version that I've been religiously using up until now:

```javascript
var foo = '123',
    bar = '789',
    baz = '000';
```

#### Why?

Let's look at commenting out lines (perhaps temporarily):

<iframe class="youtube" width="420" height="315" src="//www.youtube-nocookie.com/embed/5gb_pKz6ljA?rel=0&autoplay=1&loop=1&showinfo=0&modestbranding=1&controls=0&playlist=5gb_pKz6ljA" frameborder="0" allowfullscreen></iframe>

as you can see it's much easier to do this in the explict multiple ```var``` version
because you don't have to care about where the line you're commenting out, copying, pasting or reordering is.

Your linter might shout at you about *too many var* statements but since your minifier will end up
producing code without multiple var statements I think it's OK to turn off that particular warning.

#### Python: trailing commas in tuples
The whole conversation came about because I was expressing my preference for always leaving 
a trailing comma on a ```python``` tuple. Not because it's easier to copy and paste but because there's
a nasty gotcha in Python's syntax which means that if you remove all but the last element of a tuple
definition then it'll no longer be a tuple unless you leave a trailing comma.

```python

t1 = (
    'a', 
    'b', 
    'c'
)
# t1 is a tuple

t2 = (
   # 'a', 
    'b', 
    'c'
)
# t2 is a tuple

t3 = (
   # 'a', 
   # 'b', 
    'c'
)
# t3 is a string... WAT?

t4 = (
  #  'a', 
  #  'b', 
    'c',
)
# t4 is a tuple

```

#### SQL: prefix comma
For all the same reasons everybody knows that SQL pros always use prefix commas.

```plpgsql
SELECT   id
        ,foo 
        ,bar 
        ,baz
FROM
        foobarbazes;
```

instead of

```plpgsql
SELECT  id,
        foo, 
        bar, 
        baz
FROM
        foobarbazes;
```