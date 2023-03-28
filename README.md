<p align="center">
  <img
    src=".github/logo.png"
    align="center"
    width="100"
    alt="360macky Bot"
    title="360macky Bot"
  />
  <h1 align="center">Marcelo Bot</h1>
</p>

<p align="center">
    🤖 Personal Twitter bot powered by GPT technology 🦄
</p>

<p align="center">
  <a href="https://www.tweepy.org">
    <img src="https://img.shields.io/static/v1?label=Tweepy&message=4.13.0&color=1DA1F2&logo=twitter" />
  </a>
</p>


## 🚀 Concept

A funny Twitter bot that generates descriptions of a person every day. The bot uses the [GPT-4 model](https://openai.com/product/gpt-4) to generate the descriptions with [Tweepy](https://www.tweepy.org/) to post on Twitter.

It also sends a notification to my WhatsApp number using [Twilio](https://www.twilio.com/), whenever the bot performs a tweet.

The purpose of this bot is to have fun, learn about Twitter API and perform some experiments with OpenAI GPT-4.

### 🤖 Current abilities

This bot has the following abilities:

- Describe owner's mood every day based on last tweet
- Answer questions in mentions
- Retweet and like owner's tweets

## 💻 Development (If you want to fork the project)

### Creating an automated Twitter account

Create a [Twitter Developer Account](https://developer.twitter.com/en/apply-for-access) and create a [Twitter Account](https://twitter.com/i/flow/signup) for the bot.

Specify that your bot is [automated with a label](https://help.twitter.com/en/using-twitter/automated-account-labels).

Get all the needed keys and tokens from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard).

### Setting up the script

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` filling the variables from the `.env.example` file.

### Creating a cron job

In Mac OS, you can use the `crontab` command to create a cron job. In Linux, you can use the `cron` command. In Windows, you can use the `Task Scheduler` to create a cron job.

For example my cron job looks like this:

```
0 10 * * * /usr/bin/python3 /Users/marcelo/Documents/GitHub/twitter_bot/main.py
```

Which means that the script will run every day at 10am.

## 📦 Deployment

You can deploy the bot on many platforms like [Google Cloud](https://cloud.google.com/), [Heroku](https://www.heroku.com/), [AWS](https://aws.amazon.com/), [Vercel](https://vercel.com/), etc.

It would only need a Python environment to run the script, and the packages installed.
