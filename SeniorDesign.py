# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# -*- coding: utf-8 -*-
#############################
#   Capstone Project 2018
#############################
#   twitter
#   username: opinionpsu
#   password: senior123
#############################
#   authors: 
#   Nick Brougher, Zechariah Castillo, Taylor Novotny, Nikos Koufos
#############################

import praw # Reddit API, you might have to pip install on first use and restart ide
import pandas as pd
import requests
import urllib
import json
import twitter
import unittest
#New Imports
################################

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import re,string

################################
from rake_nltk import Rake


# Twitter keys
tw_consumer_key = "NUw4vNInQbQwuJxpUWqwpH9Qf"
tw_consumer_secret = "mICLV2cokUoTqPRJokrYftJPnqqD0lcdNSDizVf5K9IWZVVVzp"
tw_access_token = "1044098405780402176-2nNytlbAYFllXj9lfvLwI9hc98WgAA"
tw_access_token_secret = "noRjMgV5o4x5bvw9Azj3E45BQ3wT8lcwllUNS4vawUy8Q"

# Reddit Keys
rd_client_id = 'mnXq68SWnf4wZA'
rd_client_secret = 'KMm4PQBfhMlHnV4Tu-fEVsrfXG4'
rd_user_agent = 'capstone123'


def strip_links(text):
    link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def initProgram():
    re = Reddit()
    ke = KeywordExtraction(re)
    Twitter(ke)
    
# ~ 'Reddit' Returns DataFrame of articles ~ #
def Reddit():
    reddit = praw.Reddit(client_id=rd_client_id, client_secret=rd_client_secret, user_agent=rd_user_agent)
    subreddit = reddit.subreddit('news') #creates object representing subreddit
    hot_articles = subreddit.controversial(limit=1) #gets list of hot submissions in subreddit
    article_df = pd.DataFrame() # DataFrame of articles
    for submission in hot_articles: #iterates through submissions, adds titles to dataframe
        article_df.at[len(article_df), 'Title'] = submission.title
    
    print("{ Article DataFrame }\n", article_df, "\n")
    return article_df
# ~ Reddit() ~ #
   
# ~ 'KeywordExtraction' Extracts N keywords from N articles ~ #
def KeywordExtraction(article_df):
    ra = Rake()
    for row in article_df.itertuples(index=True, name='Pandas'):
        article = getattr(row, 'Title')
        print("Performing Keyword Extraction on this article: \n[", article, "]\n")
        keywords = ra.extract_keywords_from_text(article)
        print(ra.get_ranked_phrases())
        #print("Ranked Phrases With Scores: ", ra.get_ranked_phrases_with_scores(), "\n")
        keywords = ra.get_ranked_phrases()
        #keyword_df.at[len(keyword_df), 'Taylor'] = keywords #error here 
        print("--------------------------------")
    return keywords
# ~ KeywordExtraction() ~ #
    
# ~ 'Twitter' Returns DataFrame of tweets related to Keyword ~ #
def Twitter(keyword_df):
    api = twitter.api.Api(consumer_key=tw_consumer_key,
                  consumer_secret=tw_consumer_secret,
                  access_token_key=tw_access_token,
                  access_token_secret=tw_access_token_secret)
    #print(api.VerifyCredentials())
    print(keyword_df[0])
    print('\n')
    #?q=from:rioferdy AND -filter:retweets AND -filter:replies&count=20&result_type=recent
    #&result_type=recent&count=10&tweet_mode=extended
    query = "q=" + keyword_df[0] + "&result_type=recent&count=10&tweet_mode=extended"
    results = api.GetSearch(raw_query=query)
    for i in range(0,9):
        delimitedText = strip_all_entities(strip_links(results[i].full_text))
        print(delimitedText)
        print('\n')
# ~ Twitter() ~ #
    
# ~ 'SentimentAnalysis' Performs Sentiment Analysis on Tweets ~ #
def SentimentAnalysis():
    print("Hello World")
# ~ SentimentAnalysis ~ #
    
# ~ 'PublicOpinion' Returns Public Opinion Based on Sentiment Analysis ~ #
def PublicOpinion():
    print("Hello World")
# ~ PublicOpinion ~ #

initProgram()

