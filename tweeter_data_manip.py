#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from slackclient import SlackClient
from config import config

slack = config(section='slack')
sc = SlackClient(slack['token'])

df_azure = pd.read_csv('data_output/df_azure.csv')
df_aws = pd.read_csv('data_output/df_aws.csv')
df_gcp = pd.read_csv('data_output/df_gcp.csv')

topAzureTwitterURL = None
topAWSTwitterURL = None
topGCPTwitterURL = None
def removeTextDuplicatesFromDataFrameAndReturnTopTweet(df):
    print('Removing Duplicates')
    df = df.sort_values('followers_count', ascending=False)
    df = df.drop_duplicates(subset='text', keep='first')
    df = df.sort_values('retweet_count', ascending=False).head()
    df = df.reset_index(drop = True)
    return df

def constructTwitterLink(tweet):
    print('Constructing Twitter URL')
    link = 'https://twitter.com/{}/status/{}'.format(tweet['screen_name'], tweet['id'])
    return link

def getTopTweet():
    top_azure_tweets = removeTextDuplicatesFromDataFrameAndReturnTopTweet(df_azure)
    top_aws_tweets = removeTextDuplicatesFromDataFrameAndReturnTopTweet(df_aws)
    top_gcp_tweets = removeTextDuplicatesFromDataFrameAndReturnTopTweet(df_gcp)

    topAzureTwitterURL = constructTwitterLink(top_azure_tweets.loc[0])
    topAWSTwitterURL = constructTwitterLink(top_aws_tweets.loc[0])
    topGCPTwitterURL = constructTwitterLink(top_gcp_tweets.loc[0])

def postToSlack():
    print('Posting to Slack')

    sc.api_call(
      "chat.postMessage",
      username = "Twitter Update",
      icon_url ="https://thumbs.dreamstime.com/z/news-cartoon-12412446.jpg",
      channel="GHWQ9P8GM",
      as_user = False,
      text="Here are todays updates on AWS, Azure, and GCP:"
    )

    sc.api_call(
      "chat.postMessage",
      channel="GHWQ9P8GM",
      username = "Twitter Update",
      icon_url ='https://thumbs.dreamstime.com/z/news-cartoon-12412446.jpg',
      as_user = False,
      text=topAWSTwitterURL
    )

    sc.api_call(
      "chat.postMessage",
      channel="GHWQ9P8GM",
      username = "Twitter Update",
      icon_url ='https://thumbs.dreamstime.com/z/news-cartoon-12412446.jpg',
      text=topAzureTwitterURL
    )

    sc.api_call(
      "chat.postMessage",
      channel="GHWQ9P8GM",
      username = "Twitter Update",
      icon_url ='https://thumbs.dreamstime.com/z/news-cartoon-12412446.jpg',
      text=topGCPTwitterURL
    )
