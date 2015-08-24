import numpy as np
import requests
import sqlite3 as sqlite
import time


def readfeed(feed_url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson', dbfile='quakeBotDB.sqlite'):
    # Read the USGS json feed and return only relavant quantities.

    resp = requests.get(feed_url)
    j = resp.json()

    # go through the json file and insert into the database
    n = len(j['features'])
    for i in xrange(n):
        dict_input = j['features'][i]['properties']
        coord = j['features'][i]['geometry']['coordinates']
        dict_input['longitude']=coord[0]
        dict_input['latitude']=coord[1]
        dict_input['depth']=coord[2]
        if valid_location(dict_input):
            
            connection = sqlite.connect(dbfile)
            cur = connection.cursor()
            tweet_test = cur.execute('SELECT tweet FROM QUAKES WHERE code == ' + dict_input['code']).fetchall()
            if  len(tweet_test)  == 0:
                print(dict_input['title'] + ' is ready to tweet')
                insertdb(dict_input)
            elif (len(tweet_test) > 0 and tweet_test[0][0]==0):
                print('tweeted')
                cur.execute("UPDATE QUAKES SET tweet = 1, tweet_time = '" 
                    + time.asctime(time.gmtime()) + 
                    "' WHERE code == " + dict_input['code'])
            connection.commit()    
            connection.close()
        
#tweet_time = ' + time.asctime(time.gmtime())
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
    #print sqlcmd
    sqlvalues = [dict_input[y] for y in dict_input.keys()]  # make sure the values come out the same order as the keys
    #print sqlvalues
    cur.execute(sqlcmd,sqlvalues)
    connection.commit()
    connection.close()

def valid_location(dict_input):
    #Checks if the location is in Washington or Southern California
    place = dict_input['place'].lower()
    gps = [dict_input[x] for x in ['latitude', 'longitude']]
    if 'washington' in place:
        return True
    elif 'california' in place and in_socal(gps):
        return True
    else:
        return False
        
def in_socal(gps):
    #Define the line between Ventura and Las Vegas to be Southen California
    #34.2750 N, 119.2278 W Ventura
    #36.1215 N, 115.1739 W Las Vegas
    slope = (36.1215 - 34.2750) / (115.1739 - 119.2278)
    y = slope * (gps[1] - 119.2278) + 34.2750
    if gps[0] < y:
        return(True)
    else:
        return(False)
    
if __name__ == '__main__':
    readfeed('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson')