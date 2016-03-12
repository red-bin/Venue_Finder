#!/usr/bin/python2.7

from collections import defaultdict,OrderedDict
import csv 
import psycopg2
import ppygis
from geopandas import GeoDataFrame
#API v2.0
#Consumer Key	k3A5nN94Y8JHFkZfdifPcQ
#Consumer Secret	ctDkexrCh3wRAH7JL0BAwTy8woU
#Token	gs6lscBxJUYqcgV7h12m-UsYEHpxicNp
#Token Secret	-2JsHYUQdHPoQ25PBPtFQ5rw-wI
#Generate new API v2.0 token/secret


# In[99]:

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key='k3A5nN94Y8JHFkZfdifPcQ',
    consumer_secret='ctDkexrCh3wRAH7JL0BAwTy8woU',
    token='gs6lscBxJUYqcgV7h12m-UsYEHpxicNp',
    token_secret='-2JsHYUQdHPoQ25PBPtFQ5rw-wI'
)

cities=['Aurora','Batavia','Chicago','Darien','Elmhurst','Naperville',
'Oakbrook Terrace','St. Charles','Warrenville','West Chicago',
'Wheaton','Wood Dale','Addison','Bartlett','Bensenville',
'Bloomingdale','Bolingbrook','Burr Ridge','Carol Stream',
'Clarendon Hills','Downers Grove','Elk Grove Village',
'Glendale Heights','Glen Ellyn','Hanover Park','Hinsdale'
,'Itasca','Lemont','Lisle','Lombard','North Glen Ellyn',
'Oak Brook','Roselle','Schaumburg','Villa Park','Wayne',
'Westmont','Willowbrook','Winfield','Woodridge']

client = Client(auth)

#Grab cities with "food" in the above cities
city_resps = defaultdict(object)

params = {
    'category': 'venues',
    'lang': 'en',
    'location': None,
    'term': 'venue'
}

for city in cities:
    params['location'] = "%s, Illinois" % city
    resp = client.search(**params)
    city_resps[city] = resp


# In[110]:

import re
def images(url):
    url = re.sub('\?.*','',url)
    url = re.sub('/biz/','/biz_photos/',url)
    print url

all_venues = []
for city, search in city_resps.items():
    city_business = [ {'address':'|'.join(b.location.address),
                       'city':b.location.city,
                       'coord':b.location.coordinate,
                      'name':b.name,
                      'rating':b.rating, 
                      'reviewcount':b.review_count,
                      'phone':b.phone,
                      'website':b.url,
                      'images':images(b.url)}
                    for b in search.businesses ]
    [ all_venues.append(citybus) for citybus in city_business ]
    

#mkdir yelp
#for url in `cat hosts.txt | sort | uniq` ; do 
#   business=`echo $url | awk -F'/' '{ print $NF}'`
#   bdir="/tmp/yelp/${business}" 
#   echo "Processing ${business}..."
#   mkdir ${bdir} 2>/dev/null && rm -rf ${bdir} && mkdir ${bdir} #you never know...
#   pushd $bdir
#   wget $url #I hate dealing with stdin/out with wget. Just letting it do its own thing..
#   popd
#   sleep 1.5 #don't 
#done


#put the below output into a file
#grep -Hri 'src="//s' * \
#    | sed 's/img .*\/\//img src="http:\/\//g' 
#    | sed 's/ width.*$//' #removing width and everything after
#    | grep -v \>$ #removes anything not touched by previous command
#    | sed 's/$/>/' #undoes the damage of the width command
#    | grep -v script #useless javascript
#    | grep -v stars_ > ~/venue_images.txt #rating info


fh = open('/tmp/alldata.csv','w')
writer = csv.DictWriter(fh, all_venues[0].keys())
writer.writeheader()
writer.writerows(all_venues)
fh.close()

fh = open('/home/matt/venue_images.txt','r')
venues = defaultdict(list)
[ venues[venue].append(img) for venue,img in [ line.strip().split(',') for line in fh.readlines() ] ]

def get_bsite(venuename):
    for b in city_business:
        if venuename in b['website']:
            print "YAY"

for venue in venues.keys():
    images = ''.join(venues[venue])
    print "<h1>%s</h1> %s" % (venue, images)
    print "<br>"
