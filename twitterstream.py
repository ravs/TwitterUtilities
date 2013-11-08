#!/usr/bin/env python

# This Script was shared as part of Intro to DataSci Course offered by University of Washington
# https://github.com/uwescience/datasci_course_materials

import oauth2 as oauth
import urllib2 as urllib
import RavsKeys

_debug = 0

oauth_token    = oauth.Token(key=RavsKeys.access_token, secret=RavsKeys.access_token_secret)
oauth_consumer = oauth.Consumer(key=RavsKeys.consumer_key, secret=RavsKeys.consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  '''
  To get twitter search uncomment this
  url = "https://api.twitter.com/1.1/search/tweets.json"
  parameters = {"q":"conf",
               "count": 100};
  '''
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip()

if __name__ == '__main__':
  fetchsamples()
