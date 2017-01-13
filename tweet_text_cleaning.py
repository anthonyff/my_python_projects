import sys
sys.path.append('/../')

import tweepy_credentials as config 
import pandas as pd
import sys
import time
import tweepy
import re

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#get only tweet text
tweet_text=[]
for idx, tweet in enumerate(tweepy.Cursor(api.search, q= '#trump').items(20)): 
    tweet_text.append(tweet.text)

clean_tweets=[]
for i in tweet_text:
    a= re.sub(r'http\S+', '', i)#removes all links
    b = re.sub(r'\RT.*?:', '', a)#removes all 'RT...:' at beginning 
    c = re.sub(r'[#]\S*','', b) #removes all #hashtags
    d= re.sub(r'[@]\S*','', c) # removes all @ symbols 
    clean_tweets.append(d)

cleaner_tweets = []
for i in clean_tweets:
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags 
                           "]+", flags=re.UNICODE)
    cleaner_tweets.append(emoji_pattern.sub(r'', i))

#spacing issues
cleanest_tweets=[]
for i in cleaner_tweets:
    y = re.sub(r'[^\w\s]','', i)
    x = y.replace('\n', '').replace('\r', '')
    w = x.replace('    ', '')
    cleanest_tweets.append(w)