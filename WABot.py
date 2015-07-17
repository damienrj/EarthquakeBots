# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:11:17 2015

@author: Damien
"""

import tweepy
import pandas as pd
class TwitterAPI:
    def __init__(self):
        df = pd.read_csv('bot_info.config', header=None, index_col=[0]).transpose()
        consumer_key = df.consumer_key
        consumer_secret = df.consumer_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = df.access_token
        access_token_secret = df.access_token_secret
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
 
    def tweet(self, message):
        self.api.update_status(status=message)
 
if __name__ == "__main__":
    twitter = TwitterAPI()
    twitter.tweet("I'm posting a tweet!")