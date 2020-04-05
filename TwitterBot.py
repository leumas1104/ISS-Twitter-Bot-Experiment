import json
import requests
import tweepy
import time
import os

os.environ['lastID'] = str(2)

try:
    while True:
        time.sleep(600)
except:
    print('Failed')

