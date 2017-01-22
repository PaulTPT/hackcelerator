#!/usr/bin/env python
import requests
import json
from sys import exit
import urllib
baseURL ="http://hackaton.ypcloud.io/search"
body='''{ "search":[{
  	"searchType":"PROXIMITY",
   "collection":"MERCHANT",
   "what": "",
   "where":{
   "type":"GEO",
   "value":"" }
   }]}'''
data_r= json.loads(body)
headers_r = {'content-type': 'application/json'}
request=data_r['search'][0]

buying="shoes"
name="Paul"
lat="45.4754418"
lon="-73.5863705"

request['what']=buying
request['where']["value"]=lat + "," + lon + ",2"
resp = requests.post(baseURL,headers=headers_r,data=json.dumps(data_r))
if resp.status_code != 200:
    print "erreur..."
    exit(-1)

ypURL=urllib.quote("http://www.yellowpages.ca/search/si/1/" + buying + "/" + lat + "%252C" +lon)
print ypURL

bitlyURL="https://api-ssl.bitly.com/v3/shorten?access_token=ae68a24213b3fd836c2894e5e201f6a8346bd6f6&longUrl="+ypURL

resp2 = requests.get(bitlyURL)
if resp2.status_code != 200:
    print "erreur..."
    exit(-1)

shortURL=resp2.json()["data"]["url"]
print resp2.json()["data"]

store= resp.json()["searchResult"][0]["merchants"][0]
print "Hey @" + name + ", you can buy " + buying + " at " + store["businessName"] + " ! List of more stores near you available here : " +shortURL
print "Once you have found what you were looking for, ask us for the best price online !"

mapURL="https://maps.googleapis.com/maps/api/staticmap?center=" + lat + "," + lon +"&size=600x300&maptype=roadmap&markers=color:red%7Clabel:D%7C" + store["centroid"] + "&markers=color:blue%7C" + lat + "," + lon + "&key=AIzaSyBCHGSrqCmae-8V5bqRbUpS3392HZjPd0g"

urllib.urlretrieve(mapURL, "./tmp/map.png")

