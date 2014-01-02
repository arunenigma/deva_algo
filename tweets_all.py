def write_all_tweets(tweets_file, tweets_all):
    tweets = tweets_file.readlines()
    for tweet in tweets:
        if len(tweet.strip()) > 0:
            tweets_all.write('<xml>' + tweet.strip() + '</xml>\n')
        else:
            #print 'TWEET ->', tweet # tweet entries that have missing fields
            pass


def main():
    fr = open('epics/yajurveda.txt', 'rb')
    fw = open('tweets_all.txt', 'wb')
    write_all_tweets(fr, fw)
    fr.close()
    fw.close()


main()