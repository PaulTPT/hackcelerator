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

import webapp2
import json
#import urllib
from google.appengine.api import urlfetch
import urlfetch
# Simple program that demonstrates how to invoke Azure ML Text Analytics API: key phrases, language and sentiment detection.
import urllib2
import urllib
import sys
import base64

from json import *
from os import *
from sys import *
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream



# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = '6b57cb9c7c3540cebdbf2807932ecd4e'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
            
input_texts = '{"documents":[{"id":"1","text":"Je veux acheter des chaussures !"},{"id":"2","text":"TAKE MY MONEY FOR SKIRTS !"},{"id":"three","text":"I want to sell a car !"},]}'

num_detect_langs = 1;

class MyStreamListener(StreamListener):

	def on_data(self, data):
		
		
		"""
		text_file = open("Output1.txt", "w", "utf-8")

		text_obj = json.loads(data)['text']

		for tweet in text_obj :
			text_file.write(tweet)
		
		text_file.close()
		"""
		#json.loads(data)['text']
		
		if (json.loads(data)['place'] is not None):
			#print('Tweet : ' + json.loads(data)['text']+'\n')
			print('Localisation : ' + json.loads(data)['place']['full_name']+'\n')
			# Detect key phrases.
			input_texts = '{"documents":[{"id":"1","text":'+'"'+json.loads(data)['text']+'"'+'}]}'
			print(input_texts, 'utf-8')
			batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
			req = urllib2.Request(batch_keyphrase_url, input_texts, headers)
			response = urllib2.urlopen(req)
			result = response.read()
			obj = json.loads(result)
			#for keyphrase_analysis in obj['documents']:
    				#print('Key phrases ' + str(keyphrase_analysis['id']) + ': ' + ', '.join(map(str,keyphrase_analysis['keyPhrases'])))
    		#rint get_text(obj['documents'][0]['keyPhrases'][0])
		else:
			print("geo was null \n")
			print(json.loads(data)['text'])
			print('\n')
		
		
			#print('Tweet : ' + json.loads(data)['text']+'\n')
			#print('Localisation : ' + json.loads(data)['place']['full_name']+'\n')
			#print('id_string : ' + json.loads(data)['id_str']+'\n')
			return True
			print('stuff\n')

	def on_error(self, status):
		print(status)



consumer_key = "CwfkD6R86RcrJjZhaigoPXPK5"
consumer_secret = "cbE57JlP2ssDFXLoMU4SrLBSd36HvgJwTWYkX7S0NYuFLo1afb"

access_token = "822874752939425792-mEmXAY7dSuNelIMjWD70VE41d2wKNZs"
access_token_secret = "58cFhLtTVJLIqt8CeWLNJy2OigVNFjAyXCPZhibbwTQC2"



def trackHashtag(hashtag):
	hashtag = '#'+ hashtag
	myStreamListener = MyStreamListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	myStream = Stream(auth, myStreamListener)
	
	#for location add paramenter locations=[-6.38,49.87,1.77,55.81]) or locations=GEOBOX_GERMANY for example
	myStream.filter(track=[hashtag], languages =['en'], async=False)





def get_text(buying):
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

		#buying="shoes"
		name="Paul"
		lat="45.4754418"
		lon="-73.5863705"

		request['what']=buying
		request['where']["value"]=lat + "," + lon + ",2"
		resp = urlfetch.fetch(method=urlfetch.POST,url=baseURL,headers=headers_r,payload=json.dumps(data_r))
		print "toto1"
		if resp.status_code != 200:
		    print "erreur..."
		    #exit(-1)

		#ypURL=urllib.quote("http://www.yellowpages.ca/search/si/1/" + buying + "/" + lat + "%252C" +lon)
		ypURL="http://www.yellowpages.ca/search/si/1/" + buying + "/" + lat + "%252C" +lon
		#print ypURL

		bitlyURL="https://api-ssl.bitly.com/v3/shorten?access_token=ae68a24213b3fd836c2894e5e201f6a8346bd6f6&longUrl="+ypURL

		resp2 = urlfetch.fetch(bitlyURL)
		if resp2.status_code != 200:
		    print "erreur..."
		    #exit(-1)

		shortURL=json.loads(resp2.content)["data"]["url"]
		#print resp2.json()["data"]

		store= json.loads(resp.content)["searchResult"][0]["merchants"][0]
		text= "Hey @" + name + ", you can buy " + buying + " at " + store["businessName"] + " ! List of more stores near you available here : " +shortURL
		#print "Once you have found what you were looking for, ask us for the best price online !"
		
		bitlyURL="https://api-ssl.bitly.com/v3/shorten?access_token=ae68a24213b3fd836c2894e5e201f6a8346bd6f6&longUrl=https://tweetfinder-yaas-static-host.cfapps.io"

		resp3 = urlfetch.fetch(bitlyURL)
		if resp3.status_code != 200:
		    print "erreur..."
		    #exit(-1)

		shortURL_store=json.loads(resp3.content)["data"]["url"]

		text2="Btw, a  little tip @" + name +". You can found the best prices for " + buying + " online here : " + shortURL_store + " ;)"
		mapURL="https://maps.googleapis.com/maps/api/staticmap?center=" + lat + "," + lon +"&size=600x300&maptype=roadmap&markers=color:red%7Clabel:D%7C" + store["centroid"] + "&markers=color:blue%7C" + lat + "," + lon + "&key=AIzaSyBCHGSrqCmae-8V5bqRbUpS3392HZjPd0g"

		#urllib.urlretrieve(mapURL, "./tmp/map.png")
		return text

trackHashtag('askYP')


class MainPage(webapp2.RequestHandler):

	def get(self):
	    self.response.headers['Content-Type'] = 'text/plain'
	    self.response.write("starting server")
	    trackHashtag('askYP')
	    

app = webapp2.WSGIApplication([
    ('/start', MainPage),
], debug=True)
