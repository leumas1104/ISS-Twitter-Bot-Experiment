import json
import requests
import tweepy
import time
import os
from flask import Flask

app = Flask(__name__)
@app.route("/")
def TwitterBot():
    
    #get Id of last responded tweet
    def getLastID():
        return int(os.environ.get('lastID'))
    
    
    print(getLastID())

    #from keys.py in the same file directory
    CONSUMER_KEY = os.environ.get('consumer_key')
    CONSUMER_SECRET = os.environ.get('consumer_secret')
    ACCESS_TOKEN = os.environ.get('access_token')
    ACCESS_TOKEN_SECRET = os.environ.get('access_token_secret')

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
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



    #overwrite last responded tweet
    def writeLastID(ID):
        url = "https://api.heroku.com/apps/testbotinf/config-vars"
        data = {"lastID": str(ID)}
        headers = {"Content-Type": "application/json","Accept": "application/vnd.heroku+json; version=3","Authorization": "Bearer " + os.environ.get('heroku_api_token')}
        requests.patch(url, data = json.dumps(data),  headers = headers)


    #search for mentions, q = querry
    tweets = api.search(q="@testBotInf1", since_id = getLastID())
    highestID = getLastID()
    unchangedID = highestID
    if not len(tweets)==0:
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
            print("Replied")
            if highestID < tweet.id:
                highestID = tweet.id
    pl = 0
    if unchangedID == highestID:
        pl = 1
    writeLastID(highestID + pl)
    print(highestID)
    print(getLastID())
    return "Working, hopefully"

if __name__ == '__main__':
    RunApp()
def RunApp():
    app.run()
