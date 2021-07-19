import pandas as pd
import requests
import json
import time
import spacy
import sys
import matplotlib.pyplot as plt
from operator import itemgetter


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


def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

def plotBagOfWords(bagOfWords, title):
    plot = []

    wordfreq = [bagOfWords.count(w) for w in bagOfWords] # a list comprehension
    for x in range(0, len(bagOfWords)):
        plot.append([bagOfWords[x], wordfreq[x]])
    seen = set()
    result = []
    for x in range(0, len(bagOfWords)):
        if bagOfWords[x] not in seen:
            seen.add(bagOfWords[x])
            result.append([bagOfWords[x], wordfreq[x]])
    res = sorted(result, key = itemgetter(1))
    x = []
    y = []
    for item in res:
        if item[1] > 1:
            x.insert(0, item[0])
            y.insert(0, item[1])
    font = {'family' : 'normal',
        'size'   : 5}
    plt.rc('font', **font)
    plt.bar(x, y)
    addlabels(x, y)
    plt.xticks(rotation=90)
    plt.title(title)
    # giving X and Y labels
    plt.xlabel("Words used")
    plt.ylabel("Number of times used in subreddit")
    plt.show()


def runCommandLineArguments():
    t = Topic(sys.argv[1], sys.argv[2])
    data = t.getPushshiftData()
    phrases = t.getSpaceyAnalysis(data)
    bagOfWords = []
    bagOfNouns = []
    bagOfVerbs = []
    plot = []

    for element in phrases:
        words = element[0].split()
        for word in words:
            bagOfWords.append(word)
        for word in element[1]:
            bagOfNouns.append(word)
        for word in element[2]:
            bagOfVerbs.append(word)

    plotBagOfWords(bagOfWords, "Total words list without single use words")
    plotBagOfWords(bagOfNouns, "Total Nouns list based on frequency")
    plotBagOfWords(bagOfVerbs, "Total Verbs list based on frequency")

    # print(bagOfWords)
    # wordfreq = [bagOfWords.count(w) for w in bagOfWords] # a list comprehension
    # nounFrequency = [bagOfNouns.count(w) for w in bagOfNouns] # a list comprehension
    # verbFrequency = [bagOfVerbs.count(w) for w in bagOfVerbs] # a list comprehension
    # print(wordfreq)
    # for x in range(0, len(bagOfWords)):
    #     plot.append([bagOfWords[x], wordfreq[x]])
    # print(plot)
    # seen = set()
    # result = []
    # for x in range(0, len(bagOfWords)):
    #     if bagOfWords[x] not in seen:
    #         seen.add(bagOfWords[x])
    #         result.append([bagOfWords[x], wordfreq[x]])
    # res = sorted(result, key = itemgetter(1))
    # print(res)
    # x = []
    # y = []
    # for item in res:
    #     if item[1] > 1:
    #         x.insert(0, item[0])
    #         y.insert(0, item[1])
    # print(x, y)
    # font = {'family' : 'normal',
    #     'size'   : 5}
    # plt.rc('font', **font)


    # plt.bar(x, y)
    # addlabels(x, y)
    # plt.xticks(rotation=90)

    # plt.title("Word Frequency")
      
    # # giving X and Y labels
    # plt.xlabel("Words used")
    # plt.ylabel("Number of times used in subreddit")

    # plt.show()

    # print(bagOfWords)
    with open("topic_results.json", "w") as jsonFile:
        json.dump(phrases, jsonFile)
    

if len(sys.argv) == 3:
    runCommandLineArguments()
else:
    print("ERROR: Invalid input for search")
    print("Usage: python3 topicSearch.py [subreddit][previous number of days to scan]")




