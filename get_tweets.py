import tweepy
import hvac
import os

# Initialize Vault client
client = hvac.Client(url=os.getenv('VAULT_ADDR'))
client.token = os.getenv('VAULT_TOKEN')

# Read secrets from Vault
secrets = client.secrets.kv.v2.read_secret_version(path='twitter')
API_KEY = secrets['data']['data']['API_KEY']
CONSUMER_SECRET = secrets['data']['data']['CONSUMER_SECRET']
ACCESS_TOKEN = secrets['data']['data']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = secrets['data']['data']['ACCESS_TOKEN_SECRET']

# Authentication
auth = tweepy.OAuthHandler(API_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

def fetch_tweets(username, count=10):
    """
    Fetch tweets from a specified Twitter username.
    
    :param username: The Twitter username to fetch tweets from.
    :param count: The number of tweets to fetch. Default is 10.
    :return: List of tweet texts.
    """
    try:
        # Fetching tweets
        tweets = api.user_timeline(screen_name=username, count=count)
        return [tweet.text for tweet in tweets]
    except tweepy.TweepError as e:
        print(f"Error: {e}")
        return []