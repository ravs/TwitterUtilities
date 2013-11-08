#!/usr/bin/env python

#python script to get term frequency in a tweet file
import sys
import json

#dict to store words with the occurrence count
termOccurrences = {}

def countTermOccurrence(fp):
	for line in fp:
		parseTweet = json.loads(line)
		#better to check for text key before proceeding
		if 'text' in parseTweet:
			tweetWords = parseTweet["text"].split(" ")
			for word in tweetWords:
				#remove hash
				if word.startswith('#'):
					word = word.lstrip('#')
				#remove dot and comma if exist
				if word.endswith(',') or word.endswith('.'):
					word = word.rstrip(',.')
				if not word.isalpha() or word.isdigit():
					continue
				if word in termOccurrences.keys():
					termOccurrences[word] += 1.0
				else:
					termOccurrences[word] = 1.0
		print termOccurrences.items()

def printTermFreq():
	print termOccurrences.items()

def main():
	tweet_file = open(sys.argv[1])
	countTermOccurrence(tweet_file)
	printTermFreq()

if __name__ == '__main__':
    main()