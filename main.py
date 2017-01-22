# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
#import urlfetch
import urllib2
import sys
import base64
import requests
import urllib

from json import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy



# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = '6b57cb9c7c3540cebdbf2807932ecd4e'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
            
input_texts = '{"documents":[{"id":"1","text":"Je veux acheter des chaussures !"},{"id":"2","text":"TAKE MY MONEY FOR SKIRTS !"},{"id":"three","text":"I want to sell a car !"},]}'

num_detect_langs = 1;

consumer_key = "jeVGNJtVVG3RCSLy3oJ8zzFzq"
consumer_secret = "MKowNKLVV8DQ25oS86Zp23khil7lKQVB9Vr1oXhovCCElyl7iS"

access_token = "823018043982888962-7cK1fjbYJQYdPuhVtarO1CRa4i4nEIG"
access_token_secret = "MG4c5VZfBHdkG1dyYTYh7ZptZn4T7xiPs3f2vmtarJjTa"
def sendTweet (tweet):
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	status = api.update_status(status=tweet)



def get_text(buying, name,lat,lon):
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

		request['what']=buying
		request['where']["value"]=lat + "," + lon + ",2"

		bitlyURL="https://api-ssl.bitly.com/v3/shorten?access_token=ae68a24213b3fd836c2894e5e201f6a8346bd6f6&longUrl=https://tweetfinder-yaas-static-host.cfapps.io"

		resp3 = requests.get(bitlyURL)
		if resp3.status_code != 200:
		    print "erreur..."
		    #exit(-1)

		shortURL_store=resp3.json()["data"]["url"]

		try:
			resp = requests.post(baseURL,headers=headers_r,data=json.dumps(data_r))
			if resp.status_code != 200:
			    print "erreur..."
			    #exit(-1)

			#ypURL=urllib.quote("http://www.yellowpages.ca/search/si/1/" + buying + "/" + lat + "%252C" +lon)
			ypURL=urllib.quote("http://www.yellowpages.ca/search/si/1/" + buying + "/" + lat + "%252C" +lon,safe='')
			#print ypURL

			bitlyURL="https://api-ssl.bitly.com/v3/shorten?access_token=ae68a24213b3fd836c2894e5e201f6a8346bd6f6&longUrl="+ypURL

			resp2 = requests.get(bitlyURL)
			if resp2.status_code != 200:
			    print "erreur..."
			    #exit(-1)

			shortURL=resp2.json()["data"]["url"]
			#print resp2.json()["data"]

			store= resp.json()["searchResult"][0]["merchants"][0]
			text= "Hey @" + name + ", you can buy " + buying + " at " + store["businessName"] + " ! List of more stores near you available here : " +shortURL
			#print "Once you have found what you were looking for, ask us for the best price online !"

			text2="Btw, a little tip @" + name +". You can find the best prices for " + buying + " online here : " + shortURL_store + " ;)"
			mapURL="https://maps.googleapis.com/maps/api/staticmap?center=" + lat + "," + lon +"&size=600x300&maptype=roadmap&markers=color:red%7Clabel:D%7C" + store["centroid"] + "&markers=color:blue%7C" + lat + "," + lon + "&key=AIzaSyBCHGSrqCmae-8V5bqRbUpS3392HZjPd0g"

		#urllib.urlretrieve(mapURL, "./tmp/map.png")
			sendTweet(text)
			sendTweet(text2)
			print text

		except :
			text="Sorry @" + name +", I didn' t understand your request. But you can find the best prices for anything here : " + shortURL_store + " ;)"
			try:
				sendTweet(text)
				print text
			except:
				print "error"



class MyStreamListener(StreamListener):

	def on_data(self, data):
		input_texts = '{"documents":[{"id":"1","text":'+'"'+json.loads(data)['text']+'"'+'}]}'
		#print(input_texts, 'utf-8')
		batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
		req = urllib2.Request(batch_keyphrase_url, input_texts, headers)
		response = urllib2.urlopen(req)
		result = response.read()
		obj = json.loads(result)
		data_js=json.loads(data)
		buy_obj=obj['documents'][0]['keyPhrases'][0]
		name=data_js['user']['screen_name']
		try:
			lat=["place"]["bounding_box"]["coordinates"][0][0][0]
			lon=["place"]["bounding_box"]["coordinates"][0][0][1]
		except:
			lat="45.4754418"
			lon="-73.5863705"

		get_text(buy_obj,name,lat,lon)

	def on_error(self, status):
		print(status)

def trackHashtag(hashtag):
	hashtag = '#'+ hashtag
	myStreamListener = MyStreamListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	myStream = Stream(auth, myStreamListener)
	
	#for location add paramenter locations=[-6.38,49.87,1.77,55.81]) or locations=GEOBOX_GERMANY for example
	myStream.filter(track=[hashtag], languages =['en'], async=False)

trackHashtag('askYP')