#!/usr/bin/env python
# Get the statuses from the members of the List
# Ravs, FALL 2013

import api
from error import TweepError
import RavsKeys
import time
import auth
import cursor

#Twitter API global instance after getting OAuth'd
auth = auth.OAuthHandler(RavsKeys.consumer_key, RavsKeys.consumer_secret)
auth.set_access_token(RavsKeys.access_token, RavsKeys.access_token_secret)
api = api.API(auth)

# Write tweets in file
conf_training_set = open("conf_training_set.txt", "w")
list_member = open("list_member.txt","w")

# Method to stop execution and enter in sleep mode for 15Min span
def standby():
	print "Doh!! Rate limit exceeded, taking a nap now!!"
	time.sleep(910)
	print "Sleeping is just waste of time, resume execution"

# Method to return remaining api calls
def remaining_rate_limit():
	try:
		return api.rate_limit_status()['resources']['lists']['/lists/statuses']['remaining']
	except:
		return 0 # Handle EC 130 Twitter is temporarily over capacity, wait then proceed

def get_list_timeline():
	try:
		# Get all the List created/owned by the authenticated user
		# for item in api.lists_all():
		# 	print item.name + " : slug = " + item.slug + " : list_id = " + str(item.id)
		# Get the members of the list 76209711 ( name = events ) Ravs's list of Conf
		for page in cursor.Cursor(api.list_members, list_id=76209711).pages():
			for member in page:
				print member.name
				list_member.write(member.name.encode('utf-8') + "\n")
		# Get the status of the list 76209711 ( name = events ) Ravs's list of Conf
		for page in cursor.Cursor(api.list_timeline, list_id=76209711).pages():
			for status in page:
				print status.text
				# Since tweets itself have new line, qoute each tweet.
				# This might be helpful in cleaning the training set.
				conf_training_set.write("\"" + status.text.encode('utf-8') + "\"" + "\n")
			if remaining_rate_limit() == 0:
				standby()
	except TweepError as e:
		print e.args

if __name__ == '__main__':
	get_list_timeline()
