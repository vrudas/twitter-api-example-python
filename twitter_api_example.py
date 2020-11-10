import csv
import os.path
from dataclasses import dataclass
from typing import List

import tweepy as tweepy
from GetOldTweets3.manager import TweetCriteria, TweetManager

TWEETS_DUMP_FILE_PATH = './tweets.csv'


@dataclass
class Tweet:
    tweet_id: int
    text: str


def init_user_tweets(username: str, tweet_fetch_count: int) -> List[Tweet]:
    if dump_file_exists():
        return load_tweets_from_dump()
    else:
        tweets = fetch_old_tweets(username, tweet_fetch_count)
        dump_tweets_to_file(tweets)
        return tweets


def load_tweets_from_dump() -> List[Tweet]:
    with open(TWEETS_DUMP_FILE_PATH, mode='r') as tweets_dump_file:
        tweets_reader = csv.reader(tweets_dump_file)
        return [Tweet(tweet_id, text) for (tweet_id, text) in tweets_reader]


def fetch_old_tweets(username: str, tweet_fetch_count: int) -> List[Tweet]:
    tweet_criteria = TweetCriteria() \
        .setUsername(username) \
        .setMaxTweets(tweet_fetch_count)

    tweets = TweetManager.getTweets(tweet_criteria)

    return [Tweet(tweet.id, tweet.text) for tweet in tweets]


def clear_dump_file():
    if dump_file_exists():
        os.remove(TWEETS_DUMP_FILE_PATH)


def dump_file_exists() -> bool:
    return os.path.isfile(TWEETS_DUMP_FILE_PATH)


def dump_tweets_to_file(tweets_for_dump: List[Tweet]):
    with open(TWEETS_DUMP_FILE_PATH, mode='w') as tweets_dump_file:
        tweets_writer = csv.writer(tweets_dump_file)

        for (tweet) in tweets_for_dump:
            tweet_row = [tweet.tweet_id, tweet.text]
            tweets_writer.writerow(tweet_row)


def filter_tweets_by_text(tweets_to_filter: List[Tweet], text_to_filter: str) -> List[Tweet]:
    return [tweet for tweet in tweets_to_filter if text_to_filter in tweet.text]


@dataclass
class TwitterAPISecrets:
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str


def read_api_secrets_from_file(file_name: str = 'secrets.txt') -> TwitterAPISecrets:
    api_key_line_index = 0
    api_secret_line_index = 1
    access_token_line_index = 2
    access_token_secret_line_index = 3

    with open(file_name, mode='r') as secrets_file:
        lines = [line for line in secrets_file]

        api_key = extract_secret_value(lines[api_key_line_index])
        api_secret = extract_secret_value(lines[api_secret_line_index])
        access_token = extract_secret_value(lines[access_token_line_index])
        access_token_secret = extract_secret_value(lines[access_token_secret_line_index])

        return TwitterAPISecrets(
            api_key,
            api_secret,
            access_token,
            access_token_secret
        )


def extract_secret_value(line: str) -> str:
    return line.split('=')[1].strip()


if __name__ == '__main__':
    user_tweets = init_user_tweets('twitter_username', 200)
    print('user_tweets_count =', len(user_tweets))

    filtered_tweets = filter_tweets_by_text(user_tweets, 'text to filter')
    print('filtered_tweets_count =', len(filtered_tweets))
