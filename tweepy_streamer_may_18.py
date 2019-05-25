from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import models
from textblob import TextBlob

import twitter_credentials

class TwitterClient():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id="@realdonaldtrump").items(num_tweets):
            t=TextBlob(tweet._json['text'])
            print t.lower(), t.sentiment
            tweets.append(tweet)
        return tweets
    
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth
        
class TwitterStreamer():
    """
For streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # Handles twitter authentication and the connection to the twitter streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
    
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener) :
    """
Basic Listener class that prints received tweets to Twitter
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'w') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status) :
        if status == 420:
            return False
        print(status)
if __name__=="__main__":

    hash_tag_list = ["Bill Gates"]
    fetched_tweets_filename = "tweets.json"
#    twitter_streamer = TwitterStreamer()
    twitter_client = TwitterClient()
    twitter_client.get_user_timeline_tweets(100)
   
#    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    
