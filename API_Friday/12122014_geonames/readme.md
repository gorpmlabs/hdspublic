# Use GeoNames.org API for fun around the world

OK.  I'll admit it.  I am a fiend for asking weird questions of data.  But a class of questions about the Earth's population has been nagging at me lately.  For starters, I have a fascination for the populations of remote places on our planet.  If you take a good look at it, while there are a lot of humans on the planet - the [fun to watch popclock at the US census](http://www.census.gov/popclock/) claims about 319M in the US and 7.2B worldwide at the time of this article - the density of humans varies widely across the world.  That estimate stands at about 35 humans per square mile (if you account for the entire planet, hospitable to humans or not), or more than triple that if you exclude the places regular humans tend to avoid, like Antarctica.

If you've spent any time looking at a map of the Earth (online or otherwise), you know it is a big place.  You probably also know that in the last four decades we have spent a tremendous amount of resources taking satellite photos of it, measuring it, tagging it, plotting it and otherwise figuring out where things are on it, including people.

Indeed, getting the population of _known_ places, is easy.  There are a ton of online resources for find the [population of Utah](http://www.census.gov/popest/index.html) or [Recife, Brazil](http://en.wikipedia.org/wiki/Recife), for example.  But what if you didn't have any particular place in mind you were looking for, or wanted to know the cities (and populations) of an arbitrary geographic region?  Well, if you're building a dataset or app to produce or consume data like this, take a look at the wonderful [GeoNames.org API](www.geonames.org). 

## What can you do with GeoNames?
The short of it is this: GeoNames.org is a low-friction, **free** (repeat _free_) API for finding places on the earth and getting information about some 10 million+ geographic names, including metadata about latitude, longitude, elevation, population and even postal codes.  An added bonus is that you can [get some (limited) weather data from weather stations](http://www.geonames.org/export/JSON-webservices.html#weatherJSON) within a given query region, if that is of interest ... but either way how cool is that?!

If you ponder long enough, you may come up with your own ways to slice and dice up the data.  Furthermore, you can spend some time looking at efficient geo-algorithms for slicing the world up into interesting chunks and asking the API for data.

Be aware that there are [daily rate limits](http://www.geonames.org/export/), but I found them to be rather generous and if you're close to those limits regularly, paying may be worth it anyway!


## What I did with GeoNames?
You can visit their site to get a flavor for what their [full API can do](http://www.geonames.org/export/web-services.html), but with the [sample code on our Github](https://github.com/gorpmlabs/hdspublic/tree/master/API_Friday/12122014_geonames) you can 

1. to take an arbitrary [bounding box](http://wiki.openstreetmap.org/wiki/Bounding_Box) and find the top 100 cities by population within that box, 
2. get the cities (from that 100) with the highest and lowest altitude, 
3. and get top 5 most and least populous places in that top 100.

If you want to get the full city list within a bounding, you might have to slice the regions up smaller once you get to more populated places (western Europe, eastern US, etc.) - the API will complain if you set the max results too high and create a query that is too expensive.

Nonetheless, my fascination with remote populations was **somewhat** satisified after I found out some information for the bounding box:

![](img/bounding_box_img.png)

	latitude: 160W to 180W
	longitude: 65N to 85N

These are some of the basic population data returned from the code :

	5 most populous cities (of top 14 in [-180,85,-160,65])
		Kotzebue, US 
			Altitude: 16 feet
			Population: 3201
		Egvekinot, RU 
			Altitude: 6 feet
			Population: 2248
		Lorino, RU 
			Altitude: 62 feet
			Population: 1450
		Selawik, US 
			Altitude: 22 feet
			Population: 829
		Point Hope, US 
			Altitude: 13 feet
			Population: 674

And some of the basic elevation data for the lowest cities in the bounding box:

	5 lowest altitude cities (of top 14 in [-180,85,-160,65])
		Kivalina, US 
			Altitude: 16 feet
			Population: 374
		Point Hope, US 
			Altitude: 13 feet
			Population: 674
		Buckland, US 
			Altitude: 13 feet
			Population: 416
		Deering, US 
			Altitude: 13 feet
			Population: 122
		Egvekinot, RU 
			Altitude: 6 feet
			Population: 2248

You may not be as excited with this result as I am, but GeoNames API is straightforward and easy to use to do basic analytics on some of your fondest geographic curiosities.  While there are many other geo-APIs like GeoNames out there, [MapQuest Open Platform API](http://open.mapquestapi.com/), [Open Street Maps](http://openstreetmap.org/), [Google Maps API ](https://developers.google.com/maps/), [Bing Maps](http://www.microsoft.com/maps/choose-your-bing-maps-API.aspx) and many others, but if you start with GeoNames, you would be well prepared to make use of the others.  Either way, have fun!

### A note about data quality
GeoNames is awesome, and if their claim is correct that they serve over 150 million data requests _per day_, then a lot of other people think the service is awesome too.  **But** being both a free and crowdsourced/crowdpoliced/aggregated data set, there are inevitabilies around data quality and accuracy that you must take into consideration if you use it.  A great deal of the data from GeoNames is of high quality, but you will need to make sure that if you use it in production or commercial environments, that the data you're getting matches the expectations of your end users.  I found a few errors that show just this point - apparently [Nishinomiya-hama, Japan](http://en.wikipedia.org/wiki/Nishinomiya,_Hy%C5%8Dgo) (population 468,925) is -32,805.11816 feet under the earth!
 	
### A final geek dive
I couldn't help it, but I wanted to know a little more about the population and altitudes in and around the Andes (Peru, Columbia, Bogota) ... so I looked up the bounding box W-90,W-60,S-30,S-10.  I was surprised that the population of some of the highest cities on the list:

	
	5 highest altitude cities (of top 59 in [-90,-30,-60,-10])
		Cerro de Pasco, PE 
			Altitude: 14209 feet
			Population: 78910
		Potosí, BO 
			Altitude: 13024 feet
			Population: 141251
		Ayaviri, PE 
			Altitude: 12752 feet
			Population: 19310
		Llallagua, BO 
			Altitude: 12729 feet
			Population: 28069
		Juliaca, PE 
			Altitude: 12565 feet
			Population: 245675
