from tweets.stream import stream_tweets_from


SAN_FRANCISCO = [-122.75,36.8,-121.75,70.8]
LIMIT = 50000
WORDS = ['technology']

def main():
	stream_tweets_from(SAN_FRANCISCO, LIMIT, WORDS)
	# TODO: on stream close, save ngram model (to file ?)

if __name__ == "__main__":
	main()
