import json
import requests
import tweepy
import time
import os

file = open('lastID','w+')
file.write("Hi")
file.close()
file = open('lastID','r')
print(file.read())

try:
    while True:
        time.sleep(600)
except:
    print('Failed')

