#!/usr/bin/env python
# Tweepy based python script to crawl your immediate network up to 5000
# nodes in Twitter.
# Ravs, FALL 2013

import tweepy
from tweepy.error import TweepError
import RavsKeys
import time
import random
import copy

#Twitter API global instance after getting OAuth'd
auth = tweepy.OAuthHandler(RavsKeys.consumer_key, RavsKeys.consumer_secret)
auth.set_access_token(RavsKeys.access_token, RavsKeys.access_token_secret)
api = tweepy.API(auth)

# Global list to store the visited user
visited = []
# Global list to store my friends
myfrnds = []

# Global files to prepare the dataset and edgelist
dataset = open("dataset.txt", "a")
edgelist = open("edgelist.txt", "a")

# Cursor based friendlist crawling method
def friend(user_id):
	# Before making call check remaining rate limit
	if remaining_rate_limit() == 0:
		standby()
	else:
		dataset.write("\n------ Start: friends of "+str(user_id)+" -----------\n")
		edgelist.write("------ Start:  Out-Edges of "+str(user_id)+" -----------\n")
		try:
			for page in tweepy.Cursor(api.friends_ids, id=user_id).pages():
				for friend in page:
					visited.append(friend)
					dataset.write("," + str(friend))
					edgelist.write(str(user_id)+","+str(friend)+"\n")
				# Before starting new iteration check remaining rate limit
				if remaining_rate_limit() == 0:
					standby()
		except TweepError as e:
			print e.args
		dataset.write("\n------ End: friends of "+str(user_id)+" -----------\n")
		edgelist.write("------ End:  Out-Edges of "+str(user_id)+" -----------\n")

# Method to return remaining api calls
def remaining_rate_limit():
	try:
		return api.rate_limit_status()['resources']['friends']['/friends/ids']['remaining']
	except:
		return 0 # Handle EC 130 Twitter is temporarily over capacity, wait then proceed

# Method to stop execution and enter in sleep mode for 15Min span
def standby():
	print "Doh!! Rate limit exceeded, taking a nap now!!"
	#dataset.write("\n Going to sleep \n")
	#edgelist.write("Going to sleep\n")
	time.sleep(910)
	print "Sleeping is just waste of time, resume execution"

# Method to check whether the user has already been crawled or not
# returns 1 if already crawled, else 0
def is_node_crawled(node_id):
	edgelist1 = open("edgelist.txt", "r")
	for line in edgelist1:
		if line.find(node_id) == 0:
			return 1 # Node_id found in edgelist
	return 0 # Node_id not found in edgelist

def main():
	# Add authenticated user in visited node and dataset
	visited.append(api.me().id)
	dataset.write(str(api.me().id))

	# Start form authenticated user and crawl immediate friends
	print "Starting to crawl your network"
	friend(api.me().id)
	print "Completed crawling your network"

	# Start crawling friend's network
	print "Starting to crawl you friend's network"
	myfrnds = copy.copy(visited) # Assignment is copy by ref in python, hence use copy api
	myfrnds.pop(0) # remove yourself
	for user_id in myfrnds:
		friend(user_id)
	print "Completed crawling your friend's network"

	# Start crawl your friend's friend's network
	print "Starting to crawl your friend's friends network"
	dataset1 = open("dataset.txt", "r")
	nodes = []
	for line in dataset1:
		if line.find("-") != 0: # consider line which starts with ids not with comments
			for ids in line.split():
			# split() splits the string using NONE {space, tab, new line, return, form feed}
				for userid in ids.split(","):
					if userid != "": # remove the empty ones
						nodes.append(userid)
	# Get 5000 random nodes from you friend's network for crawling
	for i in range(5000):
		index = random.randrange(api.me().friends_count,len(nodes)) # randomly select node excluding yourself and your friends
		print str(i) + ": Starting to crawl node : " + str(nodes[index])
		if is_node_crawled(nodes[index]) == 0: # Node not crawled yet
			# Crawl only if the node has not been crawled yet
			friend(nodes[index])
		print str(i) + ": Completed crwaling node: " + str(nodes[index])
	print "Completed crawling your friend's friends network"
	print "Visited Nodes"
	print visited

if __name__ == '__main__':
	main()