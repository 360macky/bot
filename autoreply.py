#!/usr/local/bin/python3

import tweepy
import logging
import openai
from utils import sent_notification_to_owner, get_tweepy_api, format_tweet
from decouple import config
import time

logger = logging.getLogger().setLevel(logging.INFO)

GPT_SYSTEM_INSTRUCTIONS_MENTION = "You are a fun bot that answers people's questions very briefly and irreverently. At the end you place an emoji. If they ask you in Spanish, answer in Spanish!"
GPT_MODEL='gpt-3.5-turbo'
INTERVAL = 120 # 2 minutes

openai.api_key = config("OPENAI_API_KEY")

def get_answer(username: str, question: str):
    """
    Get answer from GPT-3.5-turbo using OpenAI API
    """
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": GPT_SYSTEM_INSTRUCTIONS_MENTION},
                {"role": "user", "content": f"Hi, my name is {username}, I'm asking: {question}?"}
            ],
            max_tokens=70
        )
        logging.info(f"GPT successfully generated anser: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except:
        logging.error("Failed to get GPT response")
        return None

def remove_bot_mention(text):
    """
    Remove bot mention from text
    """
    return ' '.join(word for word in text.split() if not word.startswith('@360mackyBOT'))

def check_mentions(api, since_id):
    """
    Check mentions, if they exists, reply to them
    """
    logging.info("Checking new mentions")
    new_since_id = since_id

    # Get mentions
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():

        # Check if we have already liked this tweet
        if tweet.favorited:
            logging.info(f"Already liked {tweet.text}")
            continue
        else:
            logging.info(f"Liking {tweet.text}")
            tweet.favorite()

        # Update the since_id
        new_since_id = max(tweet.id, new_since_id)

        # Ignore replies
        if tweet.in_reply_to_status_id is not None:
            continue


        if not tweet.user.following:
            tweet.user.follow()

        user_question = remove_bot_mention(tweet.text)

        logging.info(f"Answering question of {user_question} to {tweet.user.name}")

        generated_answer = format_tweet(get_answer(tweet.user.name, user_question))

        if generated_answer is None:
            sent_notification_to_owner(f"🤖 *Marcelo Bot* failed to generated an answer to *{user_question}*")
            continue
        
        try:
            api.update_status(
            status=generated_answer,
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,
            )
            sent_notification_to_owner(f"🤖 *Marcelo Bot* answered the question *{user_question}* to *{tweet.user.name}* with *{generated_answer}*")
        except:
            sent_notification_to_owner(f"🤖 *Marcelo Bot* failed to answer the question *{user_question}* to *{tweet.user.name}*")

    return new_since_id

def main():
    api = get_tweepy_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logging.info("Waiting for new mentions...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
