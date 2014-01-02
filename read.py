class ReadTweets(object):
    def __init__(self, tweets):
        self.tweets = tweets

    def read_file(self, tweets_file):
        """
            reading tweets and writing 1000 tweets into a new file for prototyping
        """
        i = 0
        tweets = tweets_file.readlines()
        for tweet in tweets:
            if len(tweet.strip()) > 0 and len(tweet.split(' ')) > 2:
                if i < 100:
                    self.tweets.write('<xml>' + tweet.strip() + '</xml>\n')
                    i += 1
                else:
                    #print 'TWEET ->', tweet # tweet entries that have missing fields
                    pass
