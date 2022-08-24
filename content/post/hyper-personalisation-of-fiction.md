---
date: 2011-08-16 00:00:00
title: Hyper-Personalisation of Fiction
tags: []
---

## A Different Take On Choose Your Own Adventure
Over the last few days I've come across three ideas which made me think about technology and the evolution of stories to make them more relevant to the reader.
What if technology gave us the tools to make a story more culturally relevant to each individual reader? 
### James' Musings on stories
My friend and fellow [tumblr](http://saladonions.tumblr.com "salad onions") James has been thinking about how an audience can control the direction of stories for some time and he pointed me to this [article](http://www.thisunrealcity.com/blog/?p=4956506195 "readers into players") which talks about a digital publishing platform called [Varytale](http://varytale.com) that allows authors to write interactive e-books.  
> We're working with established authors, agents and publishers, to create new works that tap the power of reader choice. We have built a set of writer's tools that allow rich narratives to weave and change, while retaining authorial and artistic control.

Cool as this idea is, I found myself thinking that I wouldn't enjoy reading one of these stories as much as I do regular fiction because when I tell a story I want to be in control and when I read a story I want to be lead through a world, and in a world crated entirely in the author's imagination the best guide is the author himself.
### The Rasputin Experiment 
In a psychology paper called [Another indirect tactic of (self-) image management](http://psp.sagepub.com/content/15/2/222.short) Finch and Ciadini. They asked a group of subjects to judge [Rasputin's deeds](http://en.wikipedia.org/wiki/Grigori_Rasputin), some were led to believe they shared the same birthday as Rasputin while others were given his real birthdate. The one's who thought they shared the same birthday produced more lenient judgements.  This got me thinking, what if you created characters who shared more than just birthdays but hometowns, schools, mutual friends with the reader? What if you did this with the antagonist but made the protagonist share nothing with the reader?

### Red Hat Installer's _Redneck_ Locale
Red Hat is an operation system, when you install it you can pick your locale (kind of like language but also with some regional and cultural elements), this flips all text in dialog boxes and prompts from the original language to one that you're more familiar with.  It has a [redneck option](http://www.ninesys.com/fun/)
[![redhat](http://farm1.static.flickr.com/174/438375208_921676dcd6_o.png)](http://www.flickr.com/photos/nicknegulescu/438375208/ "Red Hat Installer")
The possibilities of using something like this in a story are quite interesting, take the following passage. 
> Jack walked into his kitchen and poured himself a glass of water.

If you knew where your reader was from you could transform that into something like:

* French: Jacques walked into his kitchen and poured himself a glass of wine
* English: Jack walked into his kitchen and made himself a cup of tea
* American: Jack walked into his kitchen and made himself a cup of coffee
* Scottish: Jock walked into his kitchen and poured himself a glass of Irn-Bru

A recent example of this is how the name of the book _Harry Potter and the Philosopher's Stone_ was changed to  _Harry Potter and the Sorcerer's Stone_ with the intention of being more culturally relevant to each audience (US/UK). 

It's already happening in other industries,  just look at Nike's ID store which allows you to customise every aspect of your trainer and have it built and dispatched to you within weeks. 
[![nikeid](http://farm1.static.flickr.com/122/284419367_97532e5d57.jpg "Nike Id by Daniel Semper")](http://www.flickr.com/photos/danielsemper/284419367/)

### A Hyper-Personalisation Tool?
So my yin to varytale's yang, a tool which lets you write stories (or maybe we should call them story skeletons) in an online editor then publish them,  but when someone comes along and they want to read it, they'll have to log-in via Facebook.  We'll then proceed to pilfer their private data and transform the skeletons into personalised stories. If a coffee shop is mentioned, we'll use the name of the coffee shop they've got most checkins at. Else we use the default word.

#### Getting Data
When I first thought of this I wanted to mine Foursquare for people's checkin data but then I saw the Rasputin experiment and I wanted the system to be much more creepy---getting your birthdate, home town, current location and even friend's names. Facebook is the best place to get all this, combined with the tiny number of people who use Foursquare in comparison. I might add 4sq integration later because their checkin data is much richer.
#### How will it work?
Here is a short story:
>  I was going about my business, it was a Friday morning and I'd taken the morning off work to collect a package which {{Royal Mail|locale}} tried to deliver at the beginning of the week.  I have no idea what is, I certainly didn't order anything. I challenged myself after picking it up, to see if I could resist opening it until after I had coffee with Dave at {{Starbucks|place/type=coffee shop}}. The post mark told me it was from {{Leicester|place/type=hometown}}.  I failed miserably of course.

##### Localisation
There are two distinct types of markup in play here. The first one is of the format {{thing|locale}}. This is a localisation marker. If the word  on the left of the pipe is recognised as localisable word it will be substituted with the appropriate local version, so for Americans that would translate to _FedEx_ or for Germans _Deutsche Post_. If the name can't be localised, it'll be left as is. 

You might be thinking where do the list of alternative terms for localisable words come from? Me too, I'm thinking that the author fills them in when he uses a new word, these get saved to a globally accessible cultural rosetta stone which other writers can tap painlessly if they're using a word that's been defined once before. Leave suggestions in the comments if you've got a good solution.

##### Personalisation 
The other type of markup is the {{_Name_|place/type=category}}. It will substitute _Name_ with a random place of the category specified from the reader's Facebook checkins, if they haven't checked in anywhere then it'll look at popular places of that category in same city as them, and finally if there are no places of that category in their city then it'll just use _Name_.

I think this is way more important than localisation, and if this tool ever manifests, then this'll be the first feature I build.

##### Feedback
At the end of every story we should ask the reader two or three questions about the story and characters to try and understand the effect the personalisation is having, especially interesting is comparing these responses between users who got a fully personalised story verses others who got the default words.

#### Writers: What do you think?
Is is something worth experimenting with, would you use this, what features would you drop, which are missing?
Leave a comment to let me know.

