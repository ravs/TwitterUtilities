#!/usr/bin/env python

import sys
import json

#sentiment-score dict variable
scores = {}

def populateSources(fp):
	for line in fp:
		term, score = line.split("\t")
		scores[term] = int(score)

def scoreTweet(fp):
	tweetScore = 0
	for line in fp:
		tweetScore = 0 #reset score
		parseTweet = json.loads(line)
		#better to check for text key before proceeding
		if 'text' in parseTweet:
			tweetWords = parseTweet["text"].split(" ")
			for word in tweetWords:
				#remove dot and comma
				if word.endswith(',') or word.endswith('.'):
					word = word.rstrip(',.')
				#remove hash
				if word.startswith('#'):
					word = word.lstrip('#')
				#ignore symbols, numerics and words with 1 and 2 char length
				if not word.isalpha() or word.isdigit() or len(word) == 1 or len(word) == 2:
					continue
				#score these words
				else:
					if word in scores.keys():
						tweetScore = tweetScore + scores.get(word)
		print tweetScore

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #populate sentiment-score dict
    populateSources(sent_file)
    scoreTweet(tweet_file)

if __name__ == '__main__':
    main()
