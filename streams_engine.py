from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener    # stream listener that prints status text
from tweepy import OAuthHandler                # handler that allows Twitter authentication
from tweepy import Stream                      # Stream module that enables 
from textblob import TextBlob      # Python library with a simple interface to perform a variety of NLP tasks.

import twitterCredentials          # Python file that contains Twitter credentials

import matplotlib.pyplot as plt  # Used to visualize/plot data on graphs
import numpy as np      # Python Library that adds support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import pandas as pd
import re
import json


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitterCredentials.API_KEY, twitterCredentials.API_SECRET_KEY)
        auth.set_access_token(twitterCredentials.ACCESS_TOKEN, twitterCredentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)
        
        


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            #print(data)
            # with open(self.fetched_tweets_filename, 'a') as tf:
            #     tf.write(data)
            # with open(self.fetched_tweets_filename, 'a') as tf:
            #     tf.write(json.dumps(data))
            #all_data = json.loads(data)       
            #tweet = all_data["text"] 
            tweetz = data       
            #username = all_data["user"]["screen_name"]
            #print((username,tweet))
            with open(fetched_tweets_filename,"a") as fid:
                fid.write(tweetz+"\n")

            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        return df

    def print_to_file(self,tweets_ext):
        pd.set_option('display.max_colwidth', 1)
        json_frame = pd.DataFrame(data=[tweet.full_text for tweet in tweets_ext], columns=['tweets'])
        
        with open(fetched_tweets_filename,"w") as fid:
            fid.write(str(json_frame))
        pd.reset_option("^display")
 
if __name__ == '__main__':

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    tweet_analyzer_ext = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    hash_tag_list = ["twittersupport"]
    fetched_tweets_filename = "tweets.json"
    twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    #tweets = api.user_timeline(screen_name="TwitterSafety", count=20)
    tweets = api.search(q='twittersupport',lang='en',result_type='popular', count=30)
    tweets_ext = api.search(q='twittersupport',lang='en',result_type='popular', tweet_mode='extended', count=30)
    
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    json_frame = tweet_analyzer_ext.print_to_file(tweets_ext)
    
    #json_frame['sentiment'] = np.array([tweet_analyzer_ext.analyze_sentiment(tweet) for tweet in json_frame['tweets']])
    print(df.head(30))

  # Time Series
    #time_likes = pd.Series(data=df['len'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), color='r')
    #plt.show()
    
    #time_favs = pd.Series(data=df['likes'].values, index=df['date'])
    #time_favs.plot(figsize=(16, 4), color='r')
    #plt.show()

    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), color='r')
    #plt.show()

    # Layered Time Series:
    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    plt.show()


