import sys
sys.path.append('/.../')
# this is the path to the location of file with twitter API keys .py file

import twitter_api_keys as config 
import pandas as pd
import time
import tweepy
import re

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
#use tweepy's built in methods to handle twitter rate limiting
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def follow_miner(text, integer):
    """search for twitter users to follow based on hashtag or text.  checks to make sure you're not
    already following them.  stores metadata/JSON response associated with tweet in data frame 
    and requires user input to follow"""
    
    print("TWEET INFO:", '\n')
    #create list of metadata associated with each tweet 
    tweet_data=[]
    for tweet in tweepy.Cursor(api.search, q= text).items(integer): 
        tweet_data.append(tweet)
    #create list of only the ids for authors of each tweet FROM tweet_data -- less API requests     
    tweet_ids=[]    
    for tweet_id in tweet_data:
        tweet_ids.append(tweet_id)
    print('Found '+  str(len(tweet_data)) + ' tweets.' + '\n')
    
    
    print('Finding friends...', '\n')
    #create list of the ids of twitter users you follow    
    friends_ids = []
    for i, friend in enumerate(tweepy.Cursor(api.friends).items()):
        friends_ids.append(friend)
    print("Found ", i, " friends.", '\n')

    """create list of tweet metadata from users you DON'T already follow FROM TWEET_DATA 
    -- less API requests""" 
    to_follow=[]
    to_follow_names=[]
    for i in tweet_data:
        if i.author.id not in friends_ids:
            to_follow.append(i)
            to_follow_names.append(i.author.screen_name)
    print('Found ' + str(len(to_follow)) + ' that you aren\'t following.', '\n')
    print("______________________________________________________________________________")
    
    #list comprehension to easily strip each keys from JSON response 
    first_col = [tweet.author.name for tweet in to_follow]
    data_set = pd.DataFrame(first_col, columns = ["PROFILE NAME:"])
    data_set["TWEET TEXT:"] = [tweet.text for tweet in to_follow]
    data_set["FOLLOWERS COUNT:"] = [tweet.author.followers_count for tweet in to_follow]
    data_set["FRIENDS COUNT:"] = [tweet.author.friends_count for tweet in to_follow]
    data_set["# OF TWEETS:"] = [tweet.author.statuses_count for tweet in to_follow]
    data_set["LOCATION:"] = [tweet.author.location for tweet in to_follow]    
    data_set["USER CREATED AT:"] = [tweet.author.created_at for tweet in to_follow]

    #create a list of potential answer choices to iterate over
    yes = ['yes','y', 'ye', 'Yes', 'YES'] 
    no = ['no','n', 'No', 'NO']
    close = ['quit', 'exit', 'stop', 'q']

    """simultaneously read data frame row and screen name for author of the tweet 
    you searched for, but aren't already following"""
    for i,j in zip(data_set.index, to_follow_names):
        print('\n\n\n\n', data_set.ix[i], '\n\n\n\n')
        answer = input('\n' + "Follow @{0}? ".format(j))
        if answer in yes:
            api.create_friendship(j) 
            print('You just followed someone')
        elif answer in no:
            print('Maybe next time...' + '\n')
        elif answer in close:
            sys.exit(0)
        elif re.match('^[a-zA-Z0-9_.-]*$', answer): 
            pass
    return True