import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from utils.settings import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

load_dotenv()


def post_tweet(tweet_text):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": tweet_text}
    auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.post(url, json=payload, auth=auth)
    return response.json()
