#!/usr/bin/env python

#python script to get top ten hash tags in a tweet file
import sys
import json

#hash tag dict variable
hashDict = {}

def countHashTags(fp):
	for line in fp:
		parseTweet = json.loads(line)
		#better to check for text key before proceeding
		if 'text' in parseTweet:
			tweetWords = parseTweet["text"].split(" ")
			for word in tweetWords:
				#hash tags
				if word.startswith('#'):
					#remove hash
					word = word.lstrip('#')
					#remove dot and comma if exist
					if word.endswith(',') or word.endswith('.'):
						word = word.rstrip(',.')
					if word in hashDict.keys():
						#print "incrementing count of "+word
						hashDict[word] += 1.0
					else:
						#print "adding "+word
						hashDict[word] = 1.0

def main():
    tweet_file = open(sys.argv[1])
    countHashTags(tweet_file)
    #sort and print top 10 hash tags
    i = 0
    for w in sorted(hashDict, key=hashDict.get, reverse=True):
    	if i == 10:
    		break
    	elif i == 9:
    		print w, hashDict[w],
    	else:
    		print w, hashDict[w]
    	i+=1

if __name__ == '__main__':
    main()