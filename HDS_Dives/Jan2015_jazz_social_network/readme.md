## Jazz Social Network Data

The data for this project is based on the site [JazzDisco.org](www.jazzdisco.org) which inspired the project write up (see hdsjd_article.md).  The initial goal is to develop the dataset and sample visualization of the data to understand how to use it for further analysis.

The data files are loaded into the CouchDB :

[http://hds.iriscouch.com/jazzdisco_albums/](http://hds.iriscouch.com/jazzdisco_albums/)

There are a number of experimental views, but the ones of interest are :


###Getting artists in this dataset

	https://hds.iriscouch.com/jazzdisco_albums/_design/artists/_view/_all?group_level=1

Will return the JSON document :

	{"rows":[
	{"key":"\"Big\" John Patton","value":0},
	{"key":"100 Gold Fingers","value":0},
	{"key":"100 Gold Fingers, Vol. 1  (All Art","value":0},
	{"key":"100 Gold Fingers, Vol. 2  (All Art","value":0},
	{"key":"A Midnight Session With The Jazz Messengers","value":0},
	{"key":"A.K. Salim","value":0},
	{"key":"Aaron Bell","value":0},
	{"key":"Abbey Lincoln","value":0},
	{"key":"Ada Moore","value":0},
	{"key":"Ahmed Abdul-Malik","value":0},
	{"key":"Airto","value":0},
	{"key":"Airto Moreira","value":0},
	{"key":"Akiko Yano","value":0},
	{"key":"Akio Sasajima","value":0},
	{"key":"Akira Ohmori","value":0},
	{"key":"Al Cohn","value":0},
	...

This is a large list (~1700) because it includes all the artists whether they're leaders or not.

###Getting collaborators
You can learn how to get the collaborators with this simple call :

	https://hds.iriscouch.com/jazzdisco_albums/_design/artists/_view/collaborators?group=true

This will give you a list of collaboration key/value pairs : 

[<*lead*>,<*sideman*>,<*sideman-position*>,<*year*>],<***frequency***>

There are 67,487 collaboration pairs, so you can imagine a very interesting network.  NOTE: due to the data not being perfect, there are duplications and where there were multiple lead artists per album,  you will have to decide for yourself how you want to handle that!

So if we wanted to find out who Herbie Hancock played with as a leadman, we simply make the call :


	https://hds.iriscouch.com/jazzdisco_albums/_design/artists/_view/collaborators?startkey=%5B%22Herbie%20Hancock%22%5D&endkey=%5B%22Herbie%20Hancock%22,{},{}%5D&group=true


with the results :

	{"rows":[
	{"key":["Herbie Hancock","Aiyb Dieng","percussion","1984"],"value":1},
	{"key":["Herbie Hancock","Albert Heath","drums","1969"],"value":2},
	{"key":["Herbie Hancock","Anthony Williams","drums","1963"],"value":6},
	{"key":["Herbie Hancock","Anton Fier","drums","1984"],"value":1},
	{"key":["Herbie Hancock","Arthur Clarke","baritone saxophone","1969"],"value":1},
	{"key":["Herbie Hancock","Bennie Maupin","alto flute","1975"],"value":1},
	{"key":["Herbie Hancock","Bennie Maupin","bass clarinet","1975"],"value":1},
	{"key":["Herbie Hancock","Bennie Maupin","bass flute","1975"],"value":1},
	{"key":["Herbie Hancock","Bennie Maupin","saxello","1975"],"value":1},
	{"key":["Herbie Hancock","Bennie Maupin","soprano","1975"],"value":1},
	{"key":["Herbie Hancock","Bennie Maupin","tenor saxophone","1975"],"value":1},
	{"key":["Herbie Hancock","Benny Powell","trombone","1969"],"value":1},
	{"key":["Herbie Hancock","Bernard Fowler","vocals","1984"],"value":1},
	{"key":["Herbie Hancock","Bernard Purdie","drums","1966"],"value":1},
	{"key":["Herbie Hancock","Bernard Purdie","drums","1969"],"value":1},
	{"key":["Herbie Hancock","Bill Summers","percussion","1975"],"value":1},
	{"key":["Herbie Hancock","Billy Butler","guitar","1966"],"value":1},
	{"key":["Herbie Hancock","Billy Butler","guitar","1969"],"value":1},
	{"key":["Herbie Hancock","Billy Higgins","drums","1962"],"value":2},
	{"key":["Herbie Hancock","Billy Higgins","drums","1985"],"value":3},
	{"key":["Herbie Hancock","Blackbird McKnight","guitar","1975"],"value":1},
	...

You can see his network is sorely missing because there was not much data entered about Herbie.

###Getting albums
Now if we want to find out the albums that Herbie and his collaborators played on (in this dataset), we call the view :

	https://hds.iriscouch.com/jazzdisco_albums/_design/albums/_view/collaborators?startkey=%5B%22Herbie%20Hancock%22%5D&endkey=%5B%22Herbie%20Hancock%22,{},{}%5D

with the results :
	
	{"id":"4f054c34ffec001f9a04e51e4c3d8dfc","key":["Herbie Hancock","Aiyb Dieng","percussion"],"value":["System","1984","Columbia FC 39478"]},
	{"id":"b543f5c133a3aa302c103315af9024a5","key":["Herbie Hancock","Albert Heath","drums"],"value":["The Complete Blue Note Sixties Sessions","1969","Blue Note 7243 4 95569 2"]},
	{"id":"b543f5c133a3aa302c103315af90291b","key":["Herbie Hancock","Albert Heath","drums"],"value":["The Prisoner","1969","Blue Note BST 84321"]},
	{"id":"b543f5c133a3aa302c103315af5fe702","key":["Herbie Hancock","Anthony Williams","drums"],"value":["My Point Of View","1963","Blue Note BLP 4126"]},
	{"id":"b543f5c133a3aa302c103315af5fef84","key":["Herbie Hancock","Anthony Williams","drums"],"value":["The Complete Blue Note Sixties Sessions","1963","Blue Note 7243 4 95569 2"]},
	{"id":"b543f5c133a3aa302c103315af7dece0","key":["Herbie Hancock","Anthony Williams","drums"],"value":["My Point Of View","1963","Blue Note BLP 4126"]},
	{"id":"b543f5c133a3aa302c103315af7df3dd","key":["Herbie Hancock","Anthony Williams","drums"],"value":["The Complete Blue Note Sixties Sessions","1963","Blue Note 7243 4 95569 2"]},
	{"id":"b543f5c133a3aa302c103315af862666","key":["Herbie Hancock","Anthony Williams","drums"],"value":["My Point Of View","1963","Blue Note BLP 4126"]},
	{"id":"b543f5c133a3aa302c103315af862828","key":["Herbie Hancock","Anthony Williams","drums"],"value":["The Complete Blue Note Sixties Sessions","1963","Blue Note 7243 4 95569 2"]},
	{"id":"4f054c34ffec001f9a04e51e4c3d8dfc","key":["Herbie Hancock","Anton Fier","drums"],"value":["System","1984","Columbia FC 39478"]},
	...

Where our view is enriched a bit with the keys [<*docid*>,<*lead*>,<*sideman*>,<*sideman-position*>],[<**album name**>,<**year**>,<**catalog-id**>], where now we can see what album they performed on together and when.  NOTE: the *catalog-id* is pretty reliable, but remember these are mostly LPs and some of them were incorrectly parsed. 

###Getting album information
Now if we want to get the full album information, you can avail yourself of CouchDB's document retrieval with :

	https://hds.iriscouch.com/jazzdisco_albums/4f054c34ffec001f9a04e51e4c3d8dfc

which yields the full album details (at least some of them):

	{"_id":"4f054c34ffec001f9a04e51e4c3d8dfc",
	 "_rev":"1-b2503f9938fa656557c70d3b8ddf5c9b",
 	 "album":"System",
	 "artist":"Herbie Hancock",
	 "personnel":{
		"Wayne Shorter":["lyricon"],
		"Aiyb Dieng":["percussion"],
		"D.ST.":["turntables"],
		"Will Alexander":["programs"],
		"Foday Musa Suso":["kora"],
		"Bernard Fowler":["vocals"],
		"Anton Fier":["drums"],
		"Henry Kaiser":["guitar"],
		"Toshinori Kondo":["speaker"]
	 },
	 "instrument":["keyboards"],
	 "year":"1984",
	 "label-id":"Columbia FC 39478"
	}

##Experimental Stuff
There is a view to get instruments and corresponding players.  It is experimental, but may be interesting if you wanted to see *who* played on a particular instrument in this dataset.

Try out :

	https://hds.iriscouch.com/jazzdisco_albums/_design/instruments/_view/artists?group=true

giving you :

	...
	{"key":["alto saxophone","Eddie Caine"],"value":5},
	{"key":["alto saxophone","Eddie Caire"],"value":1},
	{"key":["alto saxophone","Eddie Meyers"],"value":1},
	{"key":["alto saxophone","Eddie Rosa"],"value":3},
	{"key":["alto saxophone","Eddie Vinson"],"value":2},
	{"key":["alto saxophone","Emerson Harper"],"value":2},
	{"key":["alto saxophone","Eric Dolphy"],"value":204},
	{"key":["alto saxophone","Eric Marienthal"],"value":2},
	{"key":["alto saxophone","Ernest McDonald"],"value":1},
	{"key":["alto saxophone","Ernie Henry"],"value":54},
	{"key":["alto saxophone","Ernie Watts"],"value":2},
	{"key":["alto saxophone","Ernst-Ludwig Petrowsky"],"value":1},
	{"key":["alto saxophone","Ferdinand Povel"],"value":4},
	{"key":["alto saxophone","Floyd Turnham"],"value":2},
	{"key":["alto saxophone","Frank Adams"],"value":1},
	{"key":["alto saxophone","Frank Morgan"],"value":5},
	{"key":["alto saxophone","Frank Porter"],"value":1},
	...

Looks like fun, let us know if you do something cool with it.
	
##Final Notes

The dataset is not perfect, but it **is hopefully useful** and valuable if you're looking to play with an interesting dataset.  You will likely find bugs and errors, but don't let that stop you from playing!
