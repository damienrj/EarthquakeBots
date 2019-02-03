#!/home/remote_damien/miniconda/bin/python
import usgs
import time
import tweepy
import pandas as pd
from mapping import *


class Quake_bot:
    def __init__(self, config_file):
        df = pd.read_csv(config_file, header=None, index_col=[0]).transpose()
        consumer_key = df.consumer_key.iloc[0]
        consumer_secret = df.consumer_secret.iloc[0]
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = df.access_token.iloc[0]
        access_token_secret = df.access_token_secret.iloc[0]
        auth.set_access_token(access_token, access_token_secret)
        self.google_api = df.google_api.iloc[0]
        self.api = tweepy.API(auth)

    def tweet(self, message, latitude, longitude):
        try:
            get_map(latitude, longitude, api=self.google_api)
            self.api.update_with_media("map.png", status=message)
        except tweepy.TweepError as e:
            print(e.message[0]["message"])


bots = {}
bots["Washington"] = Quake_bot("/app/data/botWA.config")
bots["California"] = Quake_bot("/app/data/botSoCal.config")
# bots['California'] =Quake_bot('botWA.config')
while True:
    usgs.readfeed(bots)
    # Twitter bot code checks for new quakes, tweets
    time.sleep(60 * 10)

# usgs.readfeed(bots, feed_url='http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson')

