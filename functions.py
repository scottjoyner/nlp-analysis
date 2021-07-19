import pandas as pd
import requests
import json
import time
import spacy


class Topic:
    def __init__(self, topic, subreddit, before, after):
        self.topic = topic
        self.subreddit = subreddit
        self.before = before
        self.after = after
        self.nlp = spacy.load("en_core_web_sm")


    def getPushshiftData(self):
        url = 'https://api.pushshift.io/reddit/search/submission?&size=1000&after='+str(self.after)+'&subreddit='+str(self.subreddit)
        r = requests.get(url)
        data = json.loads(r.text)
        return data['data']

    # Gets subreddit data that falls within the given parameters
    def getPushshiftData2(self):
        # url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(self.topic)+'&size=1000&after='+str(self.after)+'&before='+str(self.before)+'&subreddit='+str(self.subreddit)
        url = 'https://api.pushshift.io/reddit/search/submission/?&size=1000&after='+str(self.after)+'&before='+str(self.before)+'&subreddit='+str(self.subreddit)
        r = requests.get(url)
        data = json.loads(r.text)
        return data['data']
    
    def getSpaceyAnalysis(self, data):
        phrases = []
        for submisson in data:
            phrases.append([submisson['title'], submisson['selftext']])
        for sentance in phrases:
            doc = self.nlp(sentance[0])
            print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
            print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        return phrases
        # doc = self.nlp(submisson['selftext'])
        # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        # for entity in doc.ents:
        #     print(entity.text, entity.label_)

test = Topic('bullish', 'btc', 1435325343, 1626704502)
data = test.getPushshiftData()
phrases = test.getSpaceyAnalysis(data)

print(phrases)



