#!/usr/bin/env python
# coding: utf-8

from configparser import ConfigParser
import twitter
from datetime import date, timedelta
from config import config
import pandas as pd
import numpy as np
import os


# Setup the Twitter Api

SEARCH_KEYWORDS='ai%20OR%20ml%20OR%20data%20OR%20science%20'

twt = config(section='twitter')

api = twitter.Api(consumer_key=twt['consumer_key'],
                  consumer_secret=twt['consumer_secret'],
                  access_token_key=twt['access_token_key'],
                  access_token_secret=twt['access_token_secret'])

# print(api.VerifyCredentials())

# Method that strips the Twitter response and only takes fields I care about into a DF
def editDataFrameToColumnsIWant(searchResults):
    print('Editing Results for only columns we want')
    COLUMNS = ['id', 'created_at', 'hashtags', 'retweet_count', 'text']
    df = pd.DataFrame.from_records(results.AsDict() for results in searchResults)
    temp_user_data = df.user.apply(lambda user: [user.get('name'), user.get('screen_name'),user.get('followers_count')]).apply(pd.Series)
    temp_user_data.columns = ['name','screen_name', 'followers_count']
    df = df.loc[:, COLUMNS]
    df = pd.concat([df, temp_user_data], axis = 1)
    df = df.astype({"id": str})
    return df


# Method to take in hashtag keyword search and how many days back you want to search
def largeHashTagDataGrab(hashtag, daysback):
    print('Search Twitter for tweets')
    firstSearch = api.GetSearch(raw_query = "q={}%23{}%20since%3A{}%20until%3A{}&src=typd&lang=en&count=100".format(SEARCH_KEYWORDS,hashtag, date.today() - timedelta(1), date.today()))
    largeResults = editDataFrameToColumnsIWant(firstSearch)
    for x in range(1,daysback):
        tempResults = api.GetSearch(raw_query = "q={}%23{}%20since%3A{}%20until%3A{}&src=typd&lang=en&count=100".format(SEARCH_KEYWORDS,hashtag, date.today() - timedelta(x+1), date.today() - timedelta(x)))
        tempDF = editDataFrameToColumnsIWant(tempResults)
        largeResults = pd.concat([largeResults, tempDF])
    return largeResults


def searchForTweets():
    print('Starting search for tweets')
    # Search for Azure, GCP, and AWS Tweets X days back
    resultsAzure = largeHashTagDataGrab('azure', 3)
    resultsGCP = largeHashTagDataGrab('gcp', 3)
    resultsAWS = largeHashTagDataGrab('aws', 3)

    if(not os.path.isdir("./data_output")):
        os.mkdir('./data_output')

    print('Saving  Twitter tweets to csv files')
    resultsAWS.to_csv('data_output/df_aws.csv', index=False)
    resultsAzure.to_csv('data_output/df_azure.csv', index=False)
    resultsGCP.to_csv('data_output/df_gcp.csv', index=False)
