# twitter-bot
twitter bot that sends slack updates with newest info on whatever hashtags and keywords you choose to search for

# Twitter API
Create a twitter account if you dont have one and create a developer account. Add the provided keys below in the Database.ini file
Resource:
https://developer.twitter.com/en/docs/tweets/search/overview.html

# Slack API
Request slack api access from the owner of your Slack group. Add the provided keys below in the Database.ini file

Resource:
https://github.com/slackapi/python-slackclient 
https://api.slack.com/custom-integrations/legacy-tokens 

# Database.ini
create a file called Database.ini and add the following to it
```
[postgresql]
host=fill in
database=fill in
user=fill in
password=fill in

[twitter]
consumer_key=fill in
consumer_secret=fill in
access_token_key=fill in
access_token_secret=fill in

[slack]
token=fill in
```
