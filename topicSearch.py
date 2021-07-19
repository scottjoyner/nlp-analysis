import pandas as pd
import requests
import json
import time
import spacy
import sys



class Topic:
    def __init__(self, subreddit, before):
        self.subreddit = subreddit
        self.before = before
        self.nlp = spacy.load("en_core_web_sm")

    def getPushshiftData(self):
        url= 'https://api.pushshift.io/reddit/search/submission?&size=1000&before='+str(self.before)+'d&subreddit='+str(self.subreddit)
        r = requests.get(url)
        data = json.loads(r.text)
        return data['data']
    
    def getSpaceyAnalysis(self, data):
        phrases = []
        output = []
        for submisson in data:
            phrases.append([submisson['title'], submisson['selftext']])
        for sentance in phrases:
            doc = self.nlp(sentance[0])
            string = sentance[0]
            nouns = [chunk.text for chunk in doc.noun_chunks]
            verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
            output.append([string, nouns, verbs])
        return output

def current_milli_time():
    return round(time.time() * 1000)


def getBeforeAndAfterTimes(days):
    before = current_milli_time()
    after = before - (86400000 * int(days))
    print(before, after)
    return [before, after]


def runCommandLineArguments():
    t = Topic(sys.argv[1], sys.argv[2])
    data = t.getPushshiftData()
    phrases = t.getSpaceyAnalysis(data)
    for element in phrases:
        print(element[0])
        print(element[1])
        print(element[2])


if len(sys.argv) == 3:
    runCommandLineArguments()
else:
    print("ERROR: Invalid input for search")
    print("Usage: python3 topicSearch.py [subreddit][previous days to scan]")
# new = runCommandLineArguments()
# 1618070767937
# test = Topic('bullish', 'eth', 5, 1626704502)
# data = test.getPushshiftData()
# phrases = test.getSpaceyAnalysis(data)

# print(phrases)



