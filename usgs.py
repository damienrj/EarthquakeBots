import numpy as np
import requests
import sqlite3 as sqlite
import time


def readfeed(
    bots,
    feed_url="http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
    dbfile="/app/data/quakeBotDB.sqlite",
):
    # Read the USGS json feed and return only relavant quantities.

    resp = requests.get(feed_url)
    j = resp.json()

    # go through the json file and insert into the database
    n = len(j["features"])
    for i in xrange(n):
        dict_input = j["features"][i]["properties"]
        coord = j["features"][i]["geometry"]["coordinates"]
        dict_input["longitude"] = coord[0]
        dict_input["latitude"] = coord[1]
        dict_input["depth"] = coord[2]
        if valid_location(dict_input):

            # Check if tweet is in datebase
            connection = sqlite.connect(dbfile)
            cur = connection.cursor()

            # Check if the quake was tweeted
            tweet_test = cur.execute(
                "SELECT tweet FROM QUAKES WHERE code == " + dict_input["code"]
            ).fetchall()
            quake_time = time.asctime(time.localtime(dict_input["time"] / 1000))[:-5]
            message = (
                str(dict_input["mag"])
                + " earthquake "
                + dict_input["place"]
                + " at "
                + quake_time
                + " PT. "
                + dict_input["url"]
            )
            print(message)

            dict_input["tweet"] = 1
            dict_input["tweet_time"] = time.asctime(time.gmtime())
            dict_input["tweet_text"] = message

            # Checks if quake was missing, or present but not tweeted

            if "Washington" in dict_input["place"] and "Washington" in bots:

                correct_bot = bots["Washington"]
            elif (
                "California" in dict_input["place"]
                or dict_input["place"].endswith(", CA")
            ) and "California" in bots:
                correct_bot = bots["California"]
            else:
                # If there is no correct bot, close the connection and continue
                connection.commit()
                connection.close()
                continue
            # Insert values into database

            if len(tweet_test) == 0:
                insertdb(dict_input)
                correct_bot.tweet(
                    message, dict_input["latitude"], dict_input["longitude"]
                )
                print(message)
                print("working")
            elif len(tweet_test) > 0 and tweet_test[0][0] == 0:
                # This section is in case a earthquake was seen but missed and
                # not tweeted about

                # Update tweet values
                cur.execute(
                    "UPDATE QUAKES SET tweet = 1, tweet_time = '"
                    + dict_input["tweet_time"]
                    + "', tweet_text = '"
                    + dict_input["tweet_text"]
                    + "' WHERE code == "
                    + dict_input["code"]
                )
                correct_bot.tweet(
                    message, dict_input["latitude"], dict_input["longitude"]
                )
                print(message)
                print("elif working")
            connection.commit()
            connection.close()


# tweet_time = ' + time.asctime(time.gmtime())
def insertdb(dict_input, dbfile="/app/data/quakeBotDB.sqlite"):
    # insert info in the database. Takes in a dictionary of keys and
    # values and inserts those into the database

    connection = sqlite.connect(dbfile)
    cur = connection.cursor()

    # construct sql query. Since keys are named the same as columns,
    # this should be simple. Should not overwrite previous info
    sqlcmd = "insert or ignore into quakes "
    sqlcmd += "(" + ",".join(dict_input.keys()) + ") "
    sqlcmd += "values (" + ",".join(["?"] * len(dict_input.keys())) + ")"
    # print sqlcmd
    sqlvalues = [
        dict_input[y] for y in dict_input.keys()
    ]  # make sure the values come out the same order as the keys
    # print sqlvalues
    cur.execute(sqlcmd, sqlvalues)
    connection.commit()
    connection.close()


def valid_location(dict_input):
    # Checks if the location is in Washington or Southern California
    place = dict_input["place"].lower()
    gps = [dict_input[x] for x in ["latitude", "longitude"]]
    if "washington" in place:
        return True
    elif ("california" in place or place.endswith(", ca")) and in_socal(gps):
        return True
    else:
        return False


def in_socal(gps):
    # Define the line between Ventura and Las Vegas to be Southen California
    # 34.2750 N, 119.2278 W Ventura
    # 36.1215 N, 115.1739 W Las Vegas
    # 35.556769 N, 121.018985 W Cambria, California
    slope = (36.1215 - 35.556769) / (-115.1739 + 121.018985)
    y = slope * (gps[1] + 121.018985) + 35.556769
    if gps[0] < y:
        return True
    else:
        return False


if __name__ == "__main__":
    print("Testing area")
