import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("TW_API_KEY")
API_SECRET_KEY = os.getenv("TW_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TW_ACCESS_TOKEN_SECRET")

def post_tweet(tweet_text):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": tweet_text}
    auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.post(url, json=payload, auth=auth)
    return response.json()