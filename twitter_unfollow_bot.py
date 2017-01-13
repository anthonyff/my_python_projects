import sys
sys.path.append('/../')
# this is the path to the location of the file ending in .py that contains twitter API keys

import twitter_api_keys as config 
import pandas as pd
import time
import tweepy
import re

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def unfollow_bot():
    '''this is a bot that will unfollow all the twitter users that you follow 
       who dont follow you back.'''

    print("Finding friends...")
    friends_data = []
    for idx, friend in enumerate(tweepy.Cursor(api.friends).items()):
        friends_data.append(friend)
        if idx % 100 == 0 and idx > 0:
            time.sleep(60)
    print("Found", len(friends_data), "friends.", '\n')
    
    friend_screen_names=[]
    for i in friends_data:
        friend_screen_names.append(i.screen_name)
        
    print("Finding followers...")    
    followers_ids = []
    for follower in tweepy.Cursor(api.followers_ids).items():
        followers_ids.append(follower)
        if idx % 100 == 0 and idx > 0:
            time.sleep(60)
    print("Found", len(followers_ids), "followers.", '\n')
        
    #if someone you follow isn't following you, unfollow them   
    for i,j in zip(friends_data, friend_screen_names):
        if i.id not in followers_ids:
            print ('\n'"Unfollowing @{0}".format(j))
            api.destroy_friendship(i.id)
            time.sleep(5)