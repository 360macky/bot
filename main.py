#!/usr/local/bin/python3

import tweepy
import openai
import logging
from decouple import config
from utils import get_tweepy_api, sent_notification_to_owner

logger = logging.getLogger().setLevel(logging.INFO)

TWITTER_USERNAME = config('TWITTER_USERNAME')
openai.api_key = config("OPENAI_API_KEY")

GPT_SYSTEM_INSTRUCTIONS_DESCRIBER = "You are a funny and sassy bot that could answer in English to make highly ethical jokes about Marcelo, a 21-year-old software engineer. Never use more than 200 characters. Always start a sentence as 'Well today Marcelo'"
GPT_MODEL='gpt-4'

def get_wrapped_prompt(prompt_text):
    """
    Get prompt text wrapped in GPT-4 instructions
    """
    return f"Today Marcelo tweeted: '{prompt_text}'.\nDescribe it with that little information using informal terms with maximum 200 characters. Only one emoji is allowed."

def get_gpt_response(tweets_text: str) -> str:
    """
    Get response from GPT-4 using OpenAI API
    """
    try:
        logging.info(f"Generating AI response")
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": GPT_SYSTEM_INSTRUCTIONS_DESCRIBER},
                {"role": "user", "content": get_wrapped_prompt(tweets_text)}
            ],
            max_tokens=70
        )
        return response.choices[0].message.content
    except:
        logging.error("Failed to get GPT response")


def remove_hashtags(text: str) -> str:
    return ' '.join(word for word in text.split() if not word.startswith('#'))

def remove_at_characters(text: str) -> str:
    return ''.join(c for c in text if c != '@')

def trim_for_tweet(text: str) -> str:
    return text[:280]

def format_tweet(text: str) -> str:
    """
    Remove hashtags (#), at (@), and trim to 280 characters for tweet
    """
    return trim_for_tweet(remove_hashtags(remove_at_characters(text)))

def main(tweepy_api):

    # Get last 4 tweets from profile including retweets
    raw_tweets = tweepy_api.user_timeline(
        screen_name=TWITTER_USERNAME, count=6, tweet_mode='extended', include_rts=True)

    tweet_liked_quantity = 0
    tweet_retweeted_quantity = 0

    # Like and retweet the tweets received from the profile
    for tweet in raw_tweets:
        try:
            tweepy_api.retweet(tweet.id)
            tweet_liked_quantity += 1
            logging.info(f"New retweeted tweet: {tweet.full_text}")
        except tweepy.TweepyException:
            logging.warning(f"Already retweeted: {tweet.full_text}")

        try:
            tweepy_api.create_favorite(tweet.id)
            tweet_retweeted_quantity += 1
            logging.error(f"New liked tweet: {tweet.full_text}")
        except tweepy.TweepyException:
            logging.warning(f"Already liked: {tweet.full_text}")

    sent_notification_to_owner(f"🤖 *Marcelo Bot* liked {tweet_liked_quantity} tweets and retweeted {tweet_retweeted_quantity} tweets")

    # Get last 5 tweets directly from profile
    logging.info("Getting tweets from profile")
    own_tweets = tweepy_api.user_timeline(
        screen_name=TWITTER_USERNAME, count=6, tweet_mode='extended', include_rts=False)

    # Make all tweets, as one string of text separated by ;
    tweets_text = ";".join([tweet.full_text for tweet in own_tweets])

    # Generate text using GPT-4, then remove hashtags and trim to 280 characters
    generated_text = format_tweet(get_gpt_response(tweets_text))
    logging.info(f"Generated tweet: {generated_text}")

    try:
        # Tweet generated text
        tweepy_api.update_status(generated_text)
        logging.info("Tweeted successfully")
        sent_notification_to_owner(f"🤖 *Marcelo Bot* tweeted: {generated_text}")
    except Exception as e:
        logging.error(f"Failed to tweet: {generated_text}")




if __name__ == "__main__":
    sent_notification_to_owner("🚀 *Marcelo Bot* starting...")
    logging.info("Starting bot")
    tweepy_api = get_tweepy_api()
    main(tweepy_api)
    sent_notification_to_owner("🤖 *Marcelo Bot* finished!")
