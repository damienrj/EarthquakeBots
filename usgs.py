import numpy as np
import requests
import sqlite3 as sqlite


def readfeed():
    # Read the USGS json feed and return only relavant quantities.
    feed_url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'

    resp = requests.get(feed_url)
    j = resp.json()


def insertdb(dict_input,dbfile='quakeBotDB.sqlite'):
    # insert info in the database. Takes in a dictionary of keys and
    # values and inserts those into the database
    
    connection = sqlite.connect(dbfile)
    cur = connection.cursor()

    # construct sql query. Since keys are named the same as columns,
    # this should be simple. Should not overwrite previous info
    sqlcmd = 'insert or ignore into quakes '
    sqlcmd += '('+','.join(dict_input.keys())+') '
    sqlcmd += 'values ('+ ','.join(['?']*len(dict_input.keys()))+')'
    print sqlcmd
    sqlvalues = [dict_input[y] for y in dict_input.keys()]  # make sure the values come out the same order as the keys
    print sqlvalues
    cur.execute(sqlcmd,sqlvalues)
    connection.commit()
    connection.close()
