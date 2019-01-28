import urllib
import sqlite3 as sqlite
import os


def get_map(latitude,longitude,size='512x512',maptype='terrain',
            markercolor='red',api_file='../google_api.key',api=None,
            zoom = 9,save_file='map.png'):

    # given a latitude and longitude, get a static map from Google
    # Maps using their API
    if api == None:
        if os.path.exists(api_file):
            api_read = open(api_file,'r')
            api = api_read.readline()
            api = api.strip()
        else:
            print 'no api key input and no key file found'
            
    url_call = "http://maps.googleapis.com/maps/api/staticmap?"+"center="+str(latitude)+","+str(longitude)+"&size="+size+"&maptype="+maptype+"&zoom="+str(zoom)+"&markers=color:"+markercolor+"%7ClabelG%7C"+str(latitude)+","+str(longitude)+"&key="+api

    urllib.urlretrieve(url_call,save_file)
    
def get_map_from_db(code,dbfile='/app/data/quakeBotDB.sqlite',**kwargs):
    # look in the database for a unique code to get the latitude and
    # longitude in order to get a map

    connection = sqlite.connect(dbfile)
    cur = connection.cursor()

    sqlquery = 'SELECT latitude,longitude FROM quakes WHERE code = ?'
    results = cur.execute(sqlquery,(code,)).fetchall()
    if len(results) > 0:
        latitude, longitude = results[0]

        get_map(latitude,longitude,**kwargs)
