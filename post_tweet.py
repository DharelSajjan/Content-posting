import requests
from requests_oauthlib import OAuth1
import random

# # Twitter API credentials (Free Tier)
API_KEY = "SzTe4lH6T90ZqANpyhx3PHJj3"
API_SECRET_KEY = "5J4LJSLjSRHgOxcaIU9yjMf52XYXCFHBEHQdKZb2w6jzvt5EsE"
ACCESS_TOKEN = "1881470657663242240-toVHeq5z13NfVnMaphtivhgVaeLcQB"
ACCESS_TOKEN_SECRET = "25xEQZSiuljfmueWP4zpTOz0jJpx06Il58CPJESmQozZc"
bearer_token= "AAAAAAAAAAAAAAAAAAAAABlvyQEAAAAAtKTY%2F4FdtHeRvJLzsd1m7%2BeaPSU%3DsFuRdzGNer79YMyg2MHBRnl6ummru5EQHzWMLfIiLXGilz5jKW"



def post_tweet(tweet_text):
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": tweet_text}
    auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    response = requests.post(url, json=payload, auth=auth)
    return response.json()