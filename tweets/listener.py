import json


#Generic Class to listen to live tweets
class TweetListener(tweepy.StreamListener):
    def __init__(self):
        self.count = 0
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        global tweetCount
        tweetCount += 1

       	f = open("runs/" + currentRunsTime + ".txt", 'a')	


        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        twitter_handle = decoded['user']['screen_name']
        tweet_text = decoded['text'].encode('ascii', 'ignore')
        count_hashtags(tweet_text)
        
        print(tweetCount)
        f.write(str(tweetCount) + "\n")
        print '@%s: %s' % (twitter_handle, tweet_text)
        f.write(str('@%s: %s' % (twitter_handle, tweet_text) + "\n"))

        printSentiment(tweet_text)
        #f.write()

        #print counter
        for k,v in  counter.most_common():
        	print("('{}':{})".format(k,v)),
        	f.write(str("('{}':{}) ".format(k,v)))

        print '\n'
        f.write(str('\n\n'))


        return True

    def on_error(self, status):
        print status
