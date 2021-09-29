from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re
import numpy as np
#np.random.seed(42)
import tweepy

 
#tweets = pd.read_csv('Training.csv')
#tweets.columns = ['Polarity', 'Tweet_ID', 'Date', 'Query', 'User_name', 'Tweet']

# Function To Extract Text of the Tweets
def cleantweets(tweet_text):
    tweet_text = re.sub(r'@[A-Za-z0-9]+', '', tweet_text) # For Removing @ Mentions
    tweet_text = re.sub(r'#', '', tweet_text) # For Removing Hashtags
    tweet_text = re.sub(r'RT[\s]+', '', tweet_text) # For Removing Retweets
    tweet_text = re.sub(r'https?:\/\/\S+', '', tweet_text) # For Removing Hyperlinks
    return tweet_text

#tweets['Tweet'] = tweets['Tweet'].apply(cleantweets)

# function to print sentiments
# of the sentence.

def sentiment_scores(tweet):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(tweet)
    print("Input Sentence is: ", tweet) 
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    print("Sentence Overall Rated As", end = " ")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
 
    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")
 
    else :
        print("Neutral")


# To Scrape Twitter


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

search_words = '#RobertDeNiro'
date_since = '2018-10-1'

#posts = tweepy.Cursor(authentication().search, q = search_words, lang = "en", since = date_since).items(1)
posts = authentication().user_timeline(screen_name = 'ElonMusk', count = 100, lang = 'en')



# Driver code
if __name__ == "__main__" :
    sentiment_scores(cleantweets(posts[1].text))
    #sentiment_scores(np.random.choice(tweets['Tweet']))
    