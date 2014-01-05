date: 2013-09-24 00:02:56.705525
title: "My Strange Loop 2013: Part 1"
tags:
  - programming
  - strangeloop
  - st louis

I have been excited about StrangeLoop for a while, I actually told somebody the
two tech conferences I've always wanted to attend were _Emerging Languages Camp_
and StrangeLoop. When I found out that ELC was merged into the _StrangeLoop_
pre-conference; I started watching the
[@strangeloop_stl](https://twitter.com/strangeloop_stl) twitter account like a
hawk for when they opened registrations. So you can guess that I had high
expectations.

Inspired by [Sean Corfield](http://corfield.org/blog/post.cfm/the-strange-loop-2013) I'm providing a summary of the sessions I attended and my takeaways along with some general
commentary about the conference.


## Emerging Languages Camp

### [Gershwin](https://github.com/gershwin/gershwin): Stack-Based Concatenative Clojure 

Daniel came up with novel way to make a stack-based language exist inside the
Clojure world with only minuscule hacking of the Clojure reader. The syntax is
inspired by Factor.  Daniel suggests using it when you are excessively using the
threading macros in Clojure.  I can see why you might do it, but is the minor
continence provided by Gershwin worth adding another language to your stack?

### Daimio

A stack-based language designed for _sharing*_.  Where sharing in this context
means letting users extend functionality of your web-apps and share those
extension with other users. The focus being on there being clearly defined
boundaries between your JavaScript and the code written by users in Daimio. You
can see a cool multiplayer turtle demo [here](http://daimio.org:8000).

### Babel: An Untyped Stack-based HLL 

Babel was introduced as a language created as a response to not being able
to trust software that you're using from the NSA/goverment/Facebook but it 
doesn't seem to give you anything that any other language does apart from having
arbitrary-precision arithmetic and crypto in the standard library. It's stack 
based and kind of inspired by Forth and Perl(???). It seems like something that 
would be fun to write an rpython interpreter for though. There was some novel 
stuff about containerising the runtimes and being able to run nested programs 
but I didn't really understand much of that.

### Noether

Noether is weird; but in a good way. It's a language that resembles an onion.  
The inner layers are highly constrained in what you can do but provide strong 
guarantees on correctness. As you move to the other layers, 
you're allowed to be more expressive (e.g. dynamic types) but you lose some of 
the guarantees.  The slides were quite theory heavy, I would have loved to seen 
a demo of the language but maybe that doesn't exist yet.  I'll be keeping an eye
on this one.


## Workshops

I booked myself in for Kipp Bradford's hardware hacking for the rest of us
workshop.  I've messed with RaspberryPi before but never done any real
embedded development so I wanted to see how to get started. His
session was great, even for someone like me who hadn't purchased the
harware kit that went along with this workshop. Kipp showed us how to
get a zigbee wireless network working between a full of arduinos.
Along with all the basics on how to get started, what to order, how to
set up the Arduino IDE. I thought it was well worth it.


## Unsessions 

In the evening there was a track of unsessions, most of which I missed because I
was grabbing a leisurely dinner. I did make it back in time for Jason Wolfe's
[unsession](https://github.com/Prismatic/schema/wiki/2013-Strange-Loop-Unsession)
about a new library for validating data schemas in a declarative style for
Clojure.  What I found interesting about this is the goal wasn't to add enforced
shape validation but rather a formalised documentation technique which could be
optionally enforced when running tests without affecting runtime.  I feel like
I'm much more likely to use this than `clojure.core.typed`.


----

## Thursday 

### Machine Learning for Relevance and Serendipity — Jenny Finkel

Jenny talked about how Prismatic are using machine learning to deliver better
article recommendations. Prismatic is an RSS reader on auto-pilot. Instead of
users manually maintaining the feeds they want to subscribe to, Prismatic slurps
in links shared by people you follow on social networks and also some preset
topics you mark as interesting.  From there the Prismatic hive mind watches how
you interact with the articles they present to you and improve suggestions using
standard machine learning techniques. 

Jenny tells us there is no _secret sauce_. Which got @PLT_HULK rather excited:

<blockquote class="twitter-tweet"><p>NEXT PERSON WHAT USE &quot;SECRET SAUCE&quot; TO DESCRIBE THEM LANGUAGE OR FRAMESWORK HULK WILL SQUIRT SRIRACHA IN THEY EYES!!</p>&mdash; PLT HULK (@PLT_Hulk) <a href="https://twitter.com/PLT_Hulk/statuses/380701122429599744">September 19, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

She went into some of the problems they've faced with training their model
including something called the Daily Mail problem.  In an earlier iteration of
Prismatic if you read an article from the Daily Mail Online then your feed would
get flooded by more Daily Mail crap. This is due to the pool of articles Prismatic thinks you'll like is much larger than the number of articles you see. So if you view a Daily Mail article then all other Daily Mail articles in the pool recieve a small boost but enough so they they dominate what you'll actually be presented with.



![prismatic](/static/images/content/my-strange-loop-2013/prismatic.jpg)

### zip Code: Unpacking Data — Scott Vokes

Scott did a great talk on how the compression algorithms we take for granted 
every day work and the research behind them (e.g. gzip, zlib, bzip2).  The great
thing about this talk was how he went through what sort of data compresses best 
with each type of compression algorithm.

![data-compression](/static/images/content/my-strange-loop-2013/data-compression.jpg)

He followed up with how he wrote a compression algorithm that worked in the 
limited memory environments of embedded computers.

### Erlang for Authoritative DNS — Anthony Eden
Anthony talked us through the challenges and misteps his company took when rolling out their *next generation* of anycast DNS services. 

They began with a powerdns setup with a Ruby/SQL backend for responding to DNS queries that required dynamic data in their response and as you can guess it didn't scale. Sure they could have thrown a million boxes at it but that doesn't really make sense as DNS is an amazingly thin margin business. 

So he decided to rewrite the ruby part in a number of languages from Python (not much quicker than Ruby), Clojure (JVM startup time and IPC) to Go (not mature/stable enough at the time). None of these provided the performance or reliability he was looking for, instead he dumped PowerDNS completely and wrote his own Erlang DNS server (open-sourced it too).

The reasons he likes Erlang/OTP for this is that it's been doing pretty similar roles at massive scale in the telco industry for decades now. The pattern-matching allow you to destructre a DNS query packet with minimal lines of code. It's fast. It behaves nicely with kv-store caches like Memcached. However they were using JSON as their serialization format and it sucks for parsing JSON (easily solved by using a C-extension).

The other cool hack they did was instead of writing their own test suite (DNS is hairy and has lots of edge cases), the reused PowerDNS' test suite and have been contributing tests back upstream.

### Rails Girls: Empowering women through code — Adriana Palacio and Laura Garcia

![railsgirls](/static/images/content/my-strange-loop-2013/railsgirls.jpg)

Adriana and Laura are both Computer Science students from Columbia and were selected to talk about their [summer of code](https://github.com/NewRosies/conductor) project as part of the RailsGirls conference outreach program to attend StrangeLoop.

If you don't already know, RailsGirls is an organisation where girls can come along to a venue and be mentored and helped with it comes to learning Rails. It's less of a classroom and more of "hey I've been trying to get this tutorial to work but I keep getting this error" and the mentors can help fix it and stop people getting frustrated.

They also have a Google style summer of code program where an open source project can get someone from the RailsGirls community to work on their code base in exchange for management, mentoring and guidance.

This is cool for many reasons as it addresses all of the following:
 
 * Not many women work in programming
 * Of those few, even fewer are involved in open source projects
 * Of those few, even fewer give talks at tech conferences

**Bonus points: Only presentation done in Beamer/LaTeX of the conference.**


### Functional Reactive Programming in Elm — Evan Czaplicki

Evan live coding a *Mario* clone to show off some of the features in Elm. One of the coolest things was `foldp` or *fold past* 
which does a `fold` not in terms of `foldl` or `foldr` on a sequence
but in terms of time (apply this fn to the state of this value at
every tick in the game and use it as input when the next tick
happens).

The interesting trade off Elm makes to enable `foldp` to work is that
it enforces a global ordering of events. I wonder what the performance
impact of this is. I question if FRP can even work for games
programming given the hacks you can do with mutable state for
performance gains.

You can watch it on [infoq](http://www.infoq.com/presentations/elm-reactive-programming).

### Clojure core.async — Rich Hickey

![core-async](/static/images/content/my-strange-loop-2013/core-async.jpg)
Another tour-de-force from Rich, this talk wasn't exactly on
`core.async` but on the wider problem of concurrent programming and
why we are able to reason about the pitfalls of concurrent programming
when we write code that needs to travel across network boundaries but
we throw all caution to the wind when working locally. His solution to
this is to use a lightweight and simple tool to provide higher level
primatives that abstract this distinction away both when working
locally and over the network. 

### Linear Logic Programming — Chris Martens

![llp](/static/images/content/my-strange-loop-2013/linear-logic-programming.jpg)

Most people here would be familiar with Prolog or Clojure's
`core.logic` which both rely on
[first-order](http://mathworld.wolfram.com/First-OrderLogic.html)
logic. Chris talks about what happens when you swap out first-order
logic for linear logic and what makes possible.

I was blown away by the possibilities for using linear logic
programming for generating stories/literature. I've kind of gone down
the rabbit hole on this topic so expect some experiments with it soon.

*Part two* will be published shortly. There's just too much to cram
 into this post.
