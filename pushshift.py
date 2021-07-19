import pandas as pd
import requests
import json
import time

def current_milli_time():
    return round(time.time() * 1000)


# def getPushshiftData(after, sub):
#     url = 'https://api.pushshift.io/reddit/search/submission?&size=1000&after='+str(after)+'&subreddit='+str(sub)
#     print(url)
#     r = requests.get(url)
#     data = json.loads(r.text)
#     return data['data']

#list of post ID's
post_ids = []
#Subreddit to query
sub='btc'
# Unix timestamp of date to crawl from.
# 2018/04/01
after = 762704502

data = getPushshiftData(after, sub)
for submission in data:
    print(submission['selftext'])

# Will run until all posts have been gathered 
# from the 'after' date up until todays date
while len(data) > 0:
    for submission in data:
        post_ids.append(submission["id"])
    # Calls getPushshiftData() with the created date of the last submission
    try:
        data = getPushshiftData(sub=sub, after=data[-1]['created_utc'])
    finally:
        break

obj = {}
obj['sub'] = sub
obj['id'] = post_ids
# Save to json for later use
with open("submissions.json", "w") as jsonFile:
    json.dump(obj, jsonFile)
