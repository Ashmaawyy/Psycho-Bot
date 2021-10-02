from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re
import numpy as np
#np.random.seed(42)
import tweepy


def cleantweets(tweet_text):
    tweet_text = re.sub(r'@[A-Za-z0-9]+', '', tweet_text) # For Removing @ Mentions
    tweet_text = re.sub(r'#', '', tweet_text) # For Removing Hashtags
    tweet_text = re.sub(r'RT[\s]+', '', tweet_text) # For Removing Retweets
    tweet_text = re.sub(r'https?:\/\/\S+', '', tweet_text) # For Removing Hyperlinks
    return tweet_text


def sentiment_scores(tweet):
 
    result = ''

 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(tweet)
    
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        result = 'Positive'
 
    elif sentiment_dict['compound'] <= - 0.05 :
        result = 'Negative'
 
    else :
        result = 'Neutral'
    
    return tweet, result



def authentication():

    log = pd.read_csv('my keys.csv')
    consumer_key = log['Value'][0]
    consumer_secret = log['Value'][1]
    access_token = log['Value'][2]
    access_token_secret = log['Value'][3]

    autheticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
    autheticate.set_access_token(access_token, access_token_secret)
    api = tweepy.API(autheticate, wait_on_rate_limit= True)
    return api

authentication()

    
def create_dict():
    posts = authentication().user_timeline(screen_name = 'EmmaWatson', count = 100, lang = 'en')

    tweets_dict = {'Positive': [], 'Negative': [], 'Neutral': []}
    
    for i in range(len(posts)):
        tweet, sentiment = sentiment_scores(cleantweets(posts[i].text))
        tweets_dict[sentiment].append(tweet)
    
    return tweets_dict

def create_mid_dataframe():
    tweets_mid_df = pd.DataFrame.from_dict(create_dict(), orient = 'index')
    tweets_mid_df = tweets_mid_df.transpose()

    return tweets_mid_df


def Build_Main_Dataframe():
    
    tweets_main_df = pd.read_csv('Tweets.csv')
    tweets_main_df = tweets_main_df.append(create_mid_dataframe(), ignore_index = True)
    tweets_main_df.to_csv('Tweets.csv')
    return tweets_main_df

def Clear_Created_csv():
    created_csv = pd.read_csv('Tweets.csv')
    created_csv.drop(created_csv.index, inplace = True)
    created_csv.to_csv('Tweets.csv')
    




# Driver code
if __name__ == "__main__" :
    #sentiment_scores(cleantweets(posts[1].text))
    #sentiment_scores(np.random.choice(tweets['Tweet']))
    #init_main_df()
    #Build_Main_Dataframe().info()
    Clear_Created_csv()


    