import tweepy
import logging
from decouple import config
from twilio.rest import Client

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


def sent_notification_to_owner(message: str) -> None:
    """
    Send notification to owner via WhatsApp
    """
    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')
    phone_number = config('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)

    client.messages.create(body=message,
                           from_='whatsapp:+14155238886',
                           to=f"whatsapp:{phone_number}"
    )


def remove_hashtags(text):
    return ' '.join(word for word in text.split() if not word.startswith('#'))

def remove_at_characters(text):
    return ''.join(c for c in text if c != '@')

def trim_for_tweet(text):
    return text[:280]

def format_tweet(text):
    """
    Remove hashtags, mentions and trim to 280 characters for tweet
    """
    return trim_for_tweet(remove_hashtags(remove_at_characters(text)))
