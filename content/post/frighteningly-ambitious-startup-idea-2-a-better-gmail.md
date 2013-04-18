date: 2013-04-01 18:11:44.367787
title: 'Frighteningly Ambitious Startup Idea #2: A Better Gmail'
tags:
  - email
  - idea

I've been frustrated with Gmail recently, not just mildly irritated
but enough to go looking for alternatives but there really isn't
anything that compares—even the [best service paid for service 
(fastmail.fm)][fm] has a web interface straight out of the 1990s. Yahoo! Mail 
and Hotmail are too advert ridden, slow and pretty bad at dealing with spam.
Outlook.com [looks stunning][outlookss] but trying to use it you;
quickly find that it takes too many clicks to accomplish anything.

## Why has this happened? 

Google built a product in 2004 that was so compelling that it made
early adopters and *thought leaders* go through the pain of switching
email address because it was free, the search was instant instead of
either being crappy or taking an age on your desktop client, *labels*
instead of folders, it was quicker than anything else, they wouldn't
delete your account if you forgot to login for a few months, and most
importantly it gave you ten times more storage than anyone else. 


A year ago Paul Graham called Gmail out his [Frighteningly Ambitious
Startup Ideas][pg1] essay.

> Whatever you build, make it fast. GMail has become painfully slow. If you
made something no better than GMail, but fast, that alone would let you start to
pull users away from GMail.

Since then we've seen pretty impressive innovation on the email client side,
with things like the beautiful [Mailbox][mbapp] or [Taskbox][tbapp] which tries
to get even closer to pg's idea of email as a task list. However we've seen
nothing on the email service front, and until we do, we'll get no closer to
replacing email. Google doesn't seem to be interested in innovating here, and
why would they be? They are still the only game in town.


## Where do we go from here?

It's 2013, the cost of 1GiB of storage is now 1/10th of what it was in 2004.
It's 2013, we don't need a monstrosity of a Java-to-JavaScript transpiling
platform like GWT to write rich JavaScript applications. It's 2013, people are
used to paying for shit on the internet.

I propose we write a new email service—let's call it **smashingmail**.  I think 
a
like-for-like clone in something like [Derbyjs][derbyjs] or [Meteor][meteor] 
wouldn't be that obscenely hard.
And most people I've spoken to agree with me. They do question how I'm going
to build a replacement for Google's web-scale awesome cloud compute
infrastructure though. 

I have no intention. 

My plan is to just fire up one [$5
Digital Ocean VPS][doprice] per user, of course the user's emails are at the
mercy of the hard drive reliability gods but that can be solved by using
[GlusterFS][gluster] across all of the VPSes and maybe some additional high 
capacity SAN nodes. 

Each VPS can run a version of their own Postfix for inbound mail, which gets 
shoved into a database (possibly PostgreSQL through [Lampson][lampson]).  On 
top of this we can build a normal webapp that mere mortals like us can iterate 
on.

### No Loading Bars

![loading bars suck dick](/static/images/content/gmail_slow_o.gif)
![notime](/static/images/content/nobody_got_time.gif)

If we write the **smashingmail** such that views can be rendered on both the 
client and the server side then we can do away with loading a huge wad of 
JavaScript and making users suffer through a loading bar.


### Target Rolling Relase Browsers Only

Google Web Toolkit is an impressive piece of engineering for abstracting away 
the browser it even outputs different code for different browser targets to get 
around compatability issues. 

That's very cool. You know what's *even* cooler? 

Not supporting crappy browsers at all. **smashingmail** would support the 
current and previous version of Firefox, Chrome, Safari and Opera. Internet 
Explorer 10 will probably work but no promises. 

### Cool URLs for People not Computers

![better urls for email](/static/images/content/gmail_better_urls.png)

We know that [URLs are for people, not computers][urls4people] so 
**smashingmail** will use human friendly urls. Why would anyone want human 
readable URLs for email? So that emails can exist as a first class citizen in 
the HTTP world.  What's the point you ask? I can think of two great advantages.

As a side effect of only supporting modern browsers we don't need to handle any 
`location.hash` nonsense so if a user hits this URL directly we can render it 
on the server.

Ponder this—you want to share something you received via email to Facebook or 
Twitter—what do you do? You could paste it into pastebin and tweet the link, 
you could paste the entire text into a Facebook update; if it was an image you 
could upload that somewhere.

What about when you get an email from a customer that you want to share with 
your whole team? You forward it on and CC in the whole team. 

Why not make it possible to share an email by making it **public** at the 
canonical URL? Then you could just tweet that link or paste it into your team's 
HipChat/Campfire/IRC channel. It would eliminate a whole class of email, which 
is a good thing as I'm a great believer in using [email as a last 
resort][email-at-angellist].

Proper URLs would also aid in automation. Say you need to keep your AWS 
invoices for tax purposes. Filter them into a label then subscribe to that 
label using a secure RSS feed?


### GPG Support by Default

Trying to use encrypted email is hard and annoying, but it doesn't have to be.  
We could build support for checking GPG signatures by default and show a little 
padlock. Users will eventually wonder how they get a little padlock next to 
their name and set up a key-pair. After they've done this we can allow them to 
send emails to other people who've got GPG setup too. 

Google can't support this in any sane way—where you don't keep your private key 
on their server because that'd prevent them from reading your email to serve 
you better adverts. If they supported a version where the mail was decrypted 
serer side then it totally defeats the purpose of the encryption.  
**smashingmail** would decrypt the emails on the client side and it'd be 
impossible for it to read anything sensitive.


### Desktop Email Clients

Using Thunderbird, Mutt or Outlook to manage your Gmail? Good luck with marking 
as spam, archiving an email or syncing starred emails. Want to see which labels 
apply to an email? NOPE. Want to mute a thread? [NOPE][mutegmail].

I know Microsoft made a huge deal about Google automatically parsing your email 
and showing your relevant adverts but my feeling was that nobody really cares 
about that for most of their emails.  For me it's a more fundamental thing at 
stake.  Google's incentives aren't aligned with yours if you're a desktop mail 
user. You're not seeing ads and you're not seeing your Google Plus 
notifications.

Considering that **smashingmail**'s incentives are aligned with yours, desktop 
emails can get all the features of the web interface without compromise and 
without breaking the spec.

There's nothing to stop us adding a *magic epilogue* to the end of the email 
that contains some action links.  These can either open up in the browser 
(provided you're logged in) and perform the action.
![magic epilogue](/static/images/content/gmail-magic-epilogue.png)
They can also be stripped out automatically on reply as the reply will go 
through our SMTP server. That way you're not polluting the thread for other 
people.

That's OK for a start, but we can also add these things using custom headers 
such as **X-Smashing-Labels** and **X-Smashing-Action-Spam** with a link 
that'll perform the action if retrieved with a HTTP POST.  Allowing mail 
clients to integrate very easily. Writing a Thunderbird extension to parse 
those headers and put action buttons directly into the toolbar would be 
trivial.


### Full-Text Search That Works

You'd think that Google could make this work but I'm often forced to use 
Thunderbird search to find an old email I know I have but Gmail can't find. Why 
is there no *Google Instant* for email? 

### Real-Time Architecture

Don't you just hate it when compose windows get out of whack? Me too.

<iframe width="100%" height="315" 
src="http://www.youtube-nocookie.com/embed/5qSh447MZGA?rel=0&html5=1" 
frameborder="0" allowfullscreen></iframe>

This is why **smashingmail** would be built on [Meteor][meteor], 
[Derby][derbyjs] or some other framework which supports optimistic UI feedback 
and real-time client/state updates.

### Sort by Spam Score

Gmail's spam filters are quite zealous and sometimes you'll find legitimate 
mail in your Spam label, I have no problem with this; but wouldn't it be nice 
to see your spam sorted by spam-score?

### Infinite Scroll

If Gmail wasn't slow as shit then Google might be able to turn on infinite 
scroll because sometimes search doesn't cut it. Imagine you can't remember 
exactly who sent you a piece of mail or any keywords but you know it was around 
the middle of last year. If could be easily found if you could quickly scroll 
through three months of email in less than a minute.

### Keeping up with the Web

This is one area where we can start advancing the state of email. There is no 
reason not to allow people to link to an external stylesheet or embed external 
web fonts in their emails; both of these things can be treated the same as 
external images and the user can be asked if they want to see these things or 
not. It's tragic that suggesting the above can be described as advancing the 
state of email but that's where we are.

### Discoverable Keyboard Shortcuts

Gmail has got fantastic keyboard shortcuts but I only use a tiny subset of 
them. **Smashingmail** would endevour to make keyboard shortcuts discoverable 
through visual feedback.

![gmail keyboard shortcut 
before](/static/images/content/gmail-kb-shortcuts1.png)

Say a chord starts with **g**; an overlay that shows you possible chord 
completions would be a great way to help people remember it for next time.

![gmail modal keyboard shortcut 
completer](/static/images/content/gmail-kb-shortcuts2.png)

## Conclusion

Innovation at the email service provider level has been stagnant since Gmail 
launched. The modern web, faster browsers, and the maturing of JavaScript mean 
we can build a comparable front end to Gmail.  The dramatic fall in cost of 
storage and computing power means we can build a back-end that can sustain 
itself on a $10-15 per month subscription basis and while that's not as cheap 
as Google can do it, it's cheap enough for people to consider it.

The gradual erosion of trust in Google, especially after the Google Reader 
shutdown, gives a competitor like **smashingmail** a chance. This post started 
off as a rant about everything that annoys me about Gmail but has turned into 
an interesting thought experiment.  

I've almost convinced myself that this is worth doing. I'd love to hear what 
you think. I'm <a href="http://twitter.com/r4vi"><span 
class="icon-twitter">r4vi</span></a>

[pg1]: http://www.paulgraham.com/ambitious.html
[medium]: https://medium.com/on-startups/55d6e81717a2
[fm]: http://fastmail.fm
[outlookss]: http://www.engadget.com/gallery/outlook-com-preview-screenshots/5182650/
[mbapp]: http://www.mailboxapp.com/
[tbapp]: http://taskbox.co/
[doprice]: https://www.digitalocean.com/pricing
[lampson]: http://lamsonproject.org/
[gluster]: http://en.wikipedia.org/wiki/GlusterFS
[urls4people]: http://www.not-implemented.com/urls-are-for-people-not-computers/
[email-at-angellist]: http://venturehacks.com/articles/no-email-at-angellist
[meteor]: http://meteor.com/
[derbyjs]: http://derbyjs.com/
[mutegmail]: 
http://www.quora.com/Gmail/Is-there-any-way-to-mute-a-thread-in-Gmail-programmatically

