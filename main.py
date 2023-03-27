import tweepy
import openai
from decouple import config

TWITTER_API_KEY = config('CONSUMER_KEY')
TWITTER_API_SECRET = config('CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = config('ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
TWITTER_USERNAME = '360macky'

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

openai.api_key = config("OPENAI_API_KEY")

GPT_SYSTEM_INSTRUCTIONS_DESCRIBER = "You are a funny and sassy bot that could answer in English to make highly ethical jokes about Marcelo, a 21-year-old software engineer. Never use more than 200 characters. Always start a sentence as 'Well today Marcelo'"
GPT_MODEL='gpt-4'

def get_wrapped_prompt(prompt_text):
    """
    Get prompt text wrapped in GPT-4 instructions
    """
    return f"Today Marcelo tweeted: '{prompt_text}'.\nDescribe it with that little information using informal terms with maximum 200 characters. Only one emoji is allowed."

def get_gpt_response(tweets_text):
    """
    Get response from GPT-4 using OpenAI API
    """
    try:
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
        print("Failed to get GPT response")



def remove_hashtags(text):
    return ' '.join(word for word in text.split() if not word.startswith('#'))

def remove_at_characters(text):
    return ''.join(c for c in text if c != '@')

def trim_for_tweet(text):
    return text[:280]

def format_tweet(text):
    """
    Remove hashtags and trim to 280 characters for tweet
    """
    return trim_for_tweet(remove_hashtags(remove_at_characters(text)))

def activate_bot():
    raw_tweets = api.user_timeline(
        screen_name=TWITTER_USERNAME, count=4, tweet_mode='extended', include_rts=True)

    for tweet in raw_tweets:
        try:
            api.retweet(tweet.id)
            print(f"Retweeted: {tweet.full_text}")
        except Exception as e:
            # Already retweeted
            pass

        try:
            api.create_favorite(tweet.id)
            print(f"Liked: {tweet.full_text}")
        except Exception as e:
            # Already liked
            pass

    # Get last 5 tweets directly from Marcelo
    own_tweets = api.user_timeline(
        screen_name=TWITTER_USERNAME, count=6, tweet_mode='extended', include_rts=False)

    # Make all tweets, as one string of text separated by ;
    tweets_text = ";".join([tweet.full_text for tweet in own_tweets])

    # Generate text using GPT-4, then remove hashtags and trim to 280 characters
    generated_text = format_tweet(get_gpt_response(tweets_text))
    print(f"Generated tweet: {generated_text}")

    try:
        api.update_status(generated_text)
        print("Tweeted successfully")
    except Exception as e:
        print(f"Failed to tweet: {generated_text}")



activate_bot()
