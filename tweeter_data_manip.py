#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from slackclient import SlackClient
from config import config

slack = config(section='slack')
sc = SlackClient(slack['token'])

def readInCsv():
    df_azure = pd.read_csv('data_output/df_azure.csv')
    getTopTweet('Azure', df_azure)
    df_aws = pd.read_csv('data_output/df_aws.csv')
    getTopTweet('AWS', df_aws)
    df_gcp = pd.read_csv('data_output/df_gcp.csv')
    getTopTweet('GCP', df_gcp)

def removeTextDuplicatesFromDataFrameAndReturnTopTweet(df):
    print('Sorting and Removing Duplicates')
    df = df.sort_values('followers_count', ascending=False)
    df = df.drop_duplicates(subset='text', keep='first')
    df = df.sort_values('retweet_count', ascending=False).head()
    df = df.reset_index(drop = True)
    return df

def constructTwitterLink(tweet):
    print('Constructing Twitter URL')
    link = 'https://twitter.com/{}/status/{}'.format(tweet['screen_name'], tweet['id'])
    return link

def getTopTweet(topic, df):
    top_tweet = removeTextDuplicatesFromDataFrameAndReturnTopTweet(df)

    top_tweet_url = [topic, constructTwitterLink(top_tweet.loc[0])]
    postToSlack(top_tweet_url)

def postToSlack(top_tweet_url):
    print('Posting to Slack')

    sc.api_call(
      "chat.postMessage",
      username = "Twitter Update",
      icon_url ="https://thumbs.dreamstime.com/z/news-cartoon-12412446.jpg",
      channel="GHWQ9P8GM",
      as_user = False,
      text="Here are todays updates on {}:".format(top_tweet_url[0])
    )

    sc.api_call(
      "chat.postMessage",
      channel="GHWQ9P8GM",
      username = "Twitter Update",
      icon_url ='https://thumbs.dreamstime.com/z/news-cartoon-12412446.jpg',
      as_user = False,
      text=top_tweet_url[1]
    )
