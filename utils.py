import tweepy
import logging
from decouple import config

logger = logging.getLogger().setLevel(logging.INFO)

def get_tweepy_api():
    """
    Get Tweepy API object ready to use
    """
    TWITTER_API_KEY = config('CONSUMER_KEY')
    TWITTER_API_SECRET = config('CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = config('ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    
    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        logging.info("Twitter API successfully connected")
    except Exception as e:
        logging.error("Error while verifying credentials", exc_info=True)
        raise e

    return api
