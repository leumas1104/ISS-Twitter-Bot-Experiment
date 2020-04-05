import json
import requests
import tweepy
import time
import os
from flask import Flask
app = Flask(__name__)
@app.route("/")
def test():
    fileName = "lastID.txt"
    print('test')
    #from keys.py in the same file directory
    CONSUMER_KEY = os.environ.get('consumer_key')
    CONSUMER_SECRET = os.environ.get('consumer_secret')
    ACCESS_TOKEN = os.environ.get('access_token')
    ACCESS_TOKEN_SECRET = os.environ.get('access_token_secret')
    print('test')

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    print('test')
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print('test')
    lastTweet = 0
    #Verify keys
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    def getISSData():
        #get ISS data
        cords = requests.get("http://api.open-notify.org/iss-now.json")
        astros = requests.get("http://api.open-notify.org/astros.json")

        position = cords.json()["iss_position"]
        people = astros.json()["people"]

        lat = position["latitude"]
        long = position["longitude"]


        #build tweet as string
        data = "ISS DATA\n\nCurrent Position:\n\n\tLatitude: " + lat + "\n\tLongitude: " + long + "\n\nCurrent Crew:\n"
        for person in people:
            data += "\n\t" + person['name']
        return data

    #get Id of last responded tweet
    def getLastID():
        try:
            file = open(fileName, 'r')
        except:
            file = open(fileName, 'w+')
            file.write(str(0))
            file.close()
            file = open(fileName, 'r')
        finally:
            ID = int(file.read())
            file.close()
            return ID

    #overwrite last responded tweet
    def writeLastID(ID):
        file = open(fileName, 'w+')
        file.write(str(ID))
        file.close()
        return


    while True:

        #search for mentions, q = querry
        tweets = api.search(q="@testBotInf1", since_id = getLastID())

        #test
        for tweet in tweets:
            print(api.get_status(tweet.id))

        #check for mentions
        for tweet in tweets:
            replyToMe = False
            skip = False
            sn = tweet.user.screen_name
            #check if it is me
            if sn == api.me().screen_name:
                skip = True
            #check if tweet contains "@testBotInf1"
            if not tweet.in_reply_to_status_id == None:
                for mention in tweet.entities["user_mentions"]:
                    if mention["screen_name"] == api.me().screen_name:
                        replyToMe = True
            if replyToMe == False:
                if tweet.text.find("@"+api.me().screen_name) == -1:
                    skip = True
            else:
                if tweet.text.count("@"+api.me().screen_name) <= 1:
                    skip = True
            if skip == True:
                print("Skipped")
                continue
            status_msg = '@{} Hello! Here you go!'.format(sn) + '\n\n' + getISSData()
            api.update_status(status_msg, in_reply_to_status_id = tweet.id)
            print("REPLIED TO: " + sn + " WITH: " + status_msg)
            if getLastID() < tweet.id:
                writeLastID(tweet.id)
        time.sleep(600)
    return


