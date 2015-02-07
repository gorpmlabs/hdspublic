I'll admit that I am a sucker for data. I'm also a sucker for jazz -- that's right, I love jazz and have grown that love since back waaay in the day when I bought my first CD ever ([Herb Alpert's "My Abstract Heart"](http://www.allmusic.com/album/my-abstract-heart-mw0000205313)). While sadly, I don't own this CD anymore, and I'm no *real* fan of Herb now, I can still enjoy his work. Of late, however, I've become more and more a "deep vault" fan ... a "collector" of the classics. While it might be arguable that [jazz is dead](http://www.washingtonpost.com/news/opinions/wp/2014/08/08/all-that-jazz-isnt-all-that-great/) or dying, the reality is that so much of the way we access historic jazz music is not leveraging the technology that other genres utilize. But more than that, because jazz spans many more decades than most other modern American music (blues/folk, excepted - modern classical excluded), it would be nice for the younger collectors like myself to access the music in a way that allowed me to understand all the key players, sidemen, albums (in and out of print) ... but today much of this knowledge is a mystery beyond hope of comprehension. Fortunately, in researching for this project, I ran into the very excellent project over at [Linked Jazz](http://www.linkedjazz.org) that might change all that "embracing modern technology" business. Perhaps in a later article I'll talk about their semantic-based approaches (which are very much necessary to get down to the harder questions). Anyway, on to the fun hackery ahead of us ...

## A Data Playground For Jazz
The good folks over at Jazz Discography [http://jazzdisco.org/](http://jazzdisco.org/) operate a website with a ton of information about the key jazz players, labels and records of the bop and post-bop era (Blue Note, Prestige, Mercury, Savoy, etc.). This site has hundreds (if not thousands) of pages of information including recording dates, locations, artists (leaders, sidemen, etc.), first and alternate take information, etc. It is truly a treasure trove of valuable information about jazz and the fine volunteers at JD have detailed some of the greatest artists and albums from the jazz genre. You will find the giants here, from Miles Davis to Sonny Rollins to Chet Baker. Their efforts have provided a fabulous start for anyone trying to get going on the jazz backfiles from the 50s and 60s (and beyond), and while not complete, enviable in thoroughness and detail from the artists, albums, personnel, dates and session data that are cataloged.

Unfortunately the JD site has no visualizations of the wealth of data on its site. Furthermore its search functions are limited, the connections between artists, labels, etc. is not at all clear and you'd basically have to be an expert already to appreciate the depth of information there.

## The Problem Setup

In a previous article I laid out some thoughts on a jazz "social network" (again see the awesome start on this at the [Linked Jazz Project](http://www.linkedjazz.org/network)) and using such a network not only to visually access the greats, but also understand who was connected with whom, when and perhaps even get down to the questions about who had long standing relationships, who were key sidemen missed, etc. This, of course, would be valuable not only for past artists, but possibly present and future one's.

A few months back when I got interested in this jazz greats "social network", I sent an inquiry to the volunteers at JD to determine if they had a database from which the site was generated, in hopes that they'd share a SQL dump and facilitate my inquiry. Unfortunately, I never heard back, but their site has a [GFDL](https://gnu.org/licenses/fdl.html) license that allows copying and redistribution. I later came to learn that the site data **might** likely have been generated from [a tool called BRIAN](http://jazzdiscography.com/Brian/index.php) that allows discographers to catalog what they love. All this is to say there is a good chance all their data is in a database *somewhere*. Check out the GitHub for this project to get more information ...

## The Data ...
If you're going to call yourself a data scientist, you will need to get used to the reality that very little of the data you're going to work with will be in ready-made form ... pour, mix and viola, the perfect dataset ready for all your analysis dreams. This is indeed pure fantasy - most of your data will be difficult to obtain, challenging to convert and disturbingly incomplete. But that's the nature of the beast and this is a beast you will learn to tame, but must concede that you will never fully control. The data for this project includes over 10,000 albums, over 60 primary artists and hundreds of side men and women.

## A Multitude of Questions, Pick A Few
If goal of this exploration is to understand the artistic activities and social networks of jazz artists, then some of the questions we might like to answer are :

* Who are the key collaborators with each of the major artists?
* Can the lineage of one lead man/woman be visualized in an interesting way?
* What was the impact of certain leaders on sidemen going solo (think Miles Davis and all the artists he worked with and helped launch solo careers)?

Though I did not spend much time looking at label data (it is in there), here are a few questions that might come out of such data explorations :

* Can the connections between labels be visualized in an interesting way?
* Did certain labels show an interest in taking greater risks in terms of new talent?

Only a few of these will be considered in this writeup, but you are free to take the code and data and have fun with it as you may - remember to give attribution to the data source (jazzdisco.org; GPDL) and share if you do something cool with it!

## Computational Desiderata 
To bound this project and writeup, we're going to focus primarily on the first question regarding collaborators. To refine this question a bit, we're going to focus on building the relationships of an artist to his or her instruments and then visualize the players on each of those instruments. As you might imagine, a graph is an appropriate way to represent this data, and while we won't dive into graph algorithms and more complex network analysis in this write up, you can rest assured that such analysis can (and should at a future time) be performed to learn even more about this fascinating data. However, in this dive, we just want to see the data in an interesting way, and will just focus on that.

## Visualizing The Network
As I've mentioned before, if you want to work with data visualization, you'll find it difficult to avoid Mike Bostock's [D3.js](http://www.d3js.org). I won't go into detail, but on the site you will find literally hundreds of example visualizations (with code), that in many cases are ready to drop your own data in to be customized.

For this project we did just that and borrowed from the [Zoomable Circle Packing recipe](http://bl.ocks.org/mbostock/7607535) to build our visualization. With this visualization you will initially see all the instruments an artist performed with on all albums (as defined by those albums in the JD dataset), and then as you click on the instrument, you will see all the players on those instruments.  The sizes of the bubbles indicate the relative frequency of albums that player contributed to.  This provides a very simple way of seeing the aggregate strength of a player's sidemen to answer things like "How many different bass players did Player X play with?" and "Who appear to be the important piano players to Player X?"  A natural extension of this is to look at the changes of these players over time (another article?).

I love Cannonball Adderley (both his on-stage personality and playing), so I am going to pick on him for the initial example. Let's take a look at what our data and the circle packing code produces :

<a href="http://hds.gorpmdev.com/site/wp-content/uploads/2015/02/ca.png"><img src="http://hds.gorpmdev.com/site/wp-content/uploads/2015/02/ca.png" alt="ca" width="647" height="641" class="alignnone size-full wp-image-139" /></a>

As we can see drums, bass, piano, sax and trumpet were core to CA's playing - his earlier work was largely quintet driven, so it is not surprising to see that he has strong relationships with a core set of drummers, bass players and pianists.  Contrast that with Chet Baker, 

<a href="http://hds.gorpmdev.com/site/wp-content/uploads/2015/02/cb.png"><img src="http://hds.gorpmdev.com/site/wp-content/uploads/2015/02/cb.png" alt="cb" width="646" height="640" class="alignnone size-full wp-image-138" /></a>

where there appear to be a lot more players in nearly every category, but look especially at the large number of piano and bass players.  Not knowing as much about Chet's playing styles and typical orientation, it is hard to know what is going on there.  Were there a larger number of albums? Personnel per album?  Unfortunately, I did not spend more time to discover the answer, but it is in the data and with a little more time and will ... the answer might unfold.  

This circle pack viz is zoomable, so you can look at who the key players were for a particular instrument. Notice when we look at Dave Brubeck's bass players, it seems Joe Morello was his go-to bassist.  If we dug deep enough, we could visualize the span of time of the relationship since the dataset does include years of collaboration!

<a href="http://hds.gorpmdev.com/site/wp-content/uploads/2015/02/db.png"><img src="http://hds.gorpmdev.com/site/wp-content/uploads/2015/02/db.png" alt="db" width="645" height="643" class="alignnone size-full wp-image-143" /></a>

You can have fun with this simple viz and detailed dataset ... carefully browse the documentation and see what might be of interest!  While not perfect, it is a great start on what could yield some interesting discoveries and new visualizations for others to learn from!  Happy Hacking!
