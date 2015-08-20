# -*- coding: utf-8 -*-
import usgs
import time


while True:
    usgs.readfeed()
    
    #Twitter bot code checks for new quakes, tweets    
    time.sleep(60*10)
    