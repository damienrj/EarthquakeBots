# -*- coding: utf-8 -*-
import usgs
import time


while True:
    usgs.readfeed('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson')
    
    #Twitter bot code checks for new quakes, tweets    
    time.sleep(60*10)
    