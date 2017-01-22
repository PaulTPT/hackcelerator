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

def get_text():
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

		mapURL="https://maps.googleapis.com/maps/api/staticmap?center=" + lat + "," + lon +"&size=600x300&maptype=roadmap&markers=color:red%7Clabel:D%7C" + store["centroid"] + "&markers=color:blue%7C" + lat + "," + lon + "&key=AIzaSyBCHGSrqCmae-8V5bqRbUpS3392HZjPd0g"

		#urllib.urlretrieve(mapURL, "./tmp/map.png")
		print text


class MainPage(webapp2.RequestHandler):

	def get(self):
	    self.response.headers['Content-Type'] = 'text/plain'
	    get_text();
	    self.response.write("hello")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
