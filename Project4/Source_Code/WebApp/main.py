# encoding= utf-8
import pickle
import time

from flask import Flask, render_template, request as flreq, json, jsonify
import urllib.request, urllib.parse
from preprocess import Preprocessor
import numpy as np, pandas as pd

app = Flask(__name__)
EC2_IP = '3.140.99.74'
# EC2_IP = 'localhost'
CORE_NAME = 'Project4'

LANG = {'English':'en', 'Hindi':'hi', 'Spanish':'es'}

QUERY_RESULT = pd.DataFrame()
SEARCH_TYPE = 0
SELECTED_LANGUAGE = ''
POI = ''

@app.route('/')
def index():
    return render_template('index1.html')


def solr_search(query):
    global QUERY_RESULT
    inurl = 'http://' + EC2_IP + ':8983/solr/' + CORE_NAME + '/select?q='
    inurl += 'tweet_text:*' + query + '*'
    # + '%20OR%20text_ru:' + solr_query
    # + '%20OR%20text_de:' + solr_query
    field = '*'
    # inurl += '%20AND%20type:r'
    # inurl += '%20&%20type:r'
    # inurl += '%20%26%20type:r'
    inurl += '&fl=' + field + '&wt=json&indent=true&rows=1000'
    print(inurl)
    # exit(10)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    QUERY_RESULT = pd.json_normalize(docs)
    # QUERY_RESULT.drop('_version_', axis=1, inplace=True)
    QUERY_RESULT.drop(['id','text_en','text_es','text_hi','poi_id','_version_'],axis=1, inplace=True)
    # print(QUERY_RESULT.columns)
    # print(QUERY_RESULT)
    # print(docs)
    # return docs


@app.route('/search', methods=["POST", "GET"])
def search():
    pp = Preprocessor()
    global QUERY_RESULT
    global SEARCH_TYPE
    global SELECTED_LANGUAGE
    global POI

    QUERY_RESULT = pd.DataFrame()
    SEARCH_TYPE = 0
    SELECTED_LANGUAGE = ''
    POI = ''
    # user_query = "इस वाक्य को हिंदी में परिवर्तित करें"
    # user_query = 'convierte esta oración a español'
    input_data = json.loads(flreq.data.decode())
    # searchkey = json.jsonify(input_data)
    # print(input_data)
    SEARCH_TYPE = input_data['val']
    if input_data['val'] == 1:
        user_query = input_data['basic']
    else:
        user_query = input_data['adsearch']
    # user_query = input_data['basic']
    solr_query = pp.get_query(user_query)
    print(solr_query)
    solr_search(solr_query)
    result = QUERY_RESULT
    result = result[result['type'] == 'r']
    if input_data['val'] == 2:
        if input_data['languageselected']['name'] != 'Choose..':
            result = result[result['tweet_lang'] == LANG[input_data['languageselected']['name']]]
            SELECTED_LANGUAGE = LANG[input_data['languageselected']['name']]
            print(SELECTED_LANGUAGE)
        if input_data['poiselected']['name'] != 'Choose..':
            result = result[result['poi_name'] == input_data['poiselected']['name']]
            POI = input_data['poiselected']['name']
            print(POI)
    return_json = {}
    temp = []
    for i in range(len(result)):
        x = pd.DataFrame.to_json(result.iloc[i])
        temp.append(json.loads(x))
    return_json['queryresult'] = temp
    return jsonify(return_json)


@app.route('/api/get-news-result', methods=["POST", "GET"])
def news():
    # time.sleep(5)
    global QUERY_RESULT
    global SEARCH_TYPE
    global SELECTED_LANGUAGE
    # print(input_data)
    result = QUERY_RESULT
    result = result[result['type'] == 'n']
    if SEARCH_TYPE == 2:
        if SELECTED_LANGUAGE != '':
            result = result[result['tweet_lang'] == SELECTED_LANGUAGE]
    # QUERY_RESULT.to_excel('query_result.xlsx', index=False)
    # formatted_docs = format_data_for_search(docs)
    # print(formatted_docs)
    # print(result)
    return_json = {}
    temp = []
    for i in range(len(result)):
        x = pd.DataFrame.to_json(result.iloc[i])
        temp.append(json.loads(x))
    return_json['queryresult'] = temp
    # return_json['queryresult'] = pd.DataFrame.to_json(QUERY_RESULT)
    # print(return_json)
    return jsonify(return_json)


@app.route('/api/get-general-result', methods=["POST","GET"])
def general():
    global QUERY_RESULT
    global SELECTED_LANGUAGE
    result = QUERY_RESULT
    result = result[result['type'] == 're']
    if SELECTED_LANGUAGE != '':
        result = result[result['tweet_lang'] == SELECTED_LANGUAGE]
    print(result)
    return_json = {}
    temp = []
    for i in range(len(result)):
        x = pd.DataFrame.to_json(result.iloc[i])
        temp.append(json.loads(x))
    return_json['queryresult'] = temp
    return jsonify(return_json)


@app.route('/api/get-chart-result')
def chart1():
    # time.sleep(5)
    global QUERY_RESULT
    global SEARCH_TYPE
    global POI
    global SELECTED_LANGUAGE
    # print("inside chart1")
    # print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    poi = result[result['type'] == 'r']
    print(poi)
    if POI != '':
        poi = poi[poi['poi_name'] == POI]
    if SELECTED_LANGUAGE != '':
        poi = poi[poi['tweet_lang'] == SELECTED_LANGUAGE]
    li = []
    for i in poi['sentiment']:
        # print(type(i))
        li.append(round(float(i), 5))
        # print(round(float(i), 5))
    # poi['sentiment'] = li
    # poi.loc[:,'sentiment'] = li
    poi = poi.assign(sentiment=li)
    # print(poi)
    ind = poi.groupby('poi_name').describe().index
    print(ind)
    graph_data = []
    for i in ind:
        data = {}
        # print(type(i),"   ",i)
        temp = poi[poi['poi_name'] == i]
        data['poi_name'] = i
        data['count'] = temp['sentiment'].mean()
        # print(data)
        graph_data.append(data)
    print(graph_data)
    return jsonify(graph_data)


@app.route('/api/get-chart-result1')
def chart2():
    global QUERY_RESULT
    global SELECTED_LANGUAGE
    # print("inside chart1")
    # print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    poi = result[result['type'] == 'r']
    if SELECTED_LANGUAGE != '':
        poi = poi[poi['tweet_lang'] == SELECTED_LANGUAGE]
    # poi = result
    # print(poi)
    lang = poi.groupby('tweet_lang').describe().index
    graph_data = []
    for i in lang:
        data = {}
        # print(type(i),"   ",i)
        temp = poi[poi['tweet_lang'] == i]
        data['language'] = i
        data['count'] = int(temp['tweet_lang'].count())
        # print(data)
        graph_data.append(data)
    # print(graph_data)
    return jsonify(graph_data)


@app.route('/api/get-chart-result2')
def chart3():
    global QUERY_RESULT
    # print("inside chart1")
    # print(QUERY_RESULT)
    # QUERY_RESULT.to_excel('query_result.xlsx')
    result = QUERY_RESULT
    # poi = result[result['type'] == 'r']
    # print(poi)
    poi = result
    lang = poi.groupby('country').describe().index
    graph_data = []
    for i in lang:
        data = {}
        # print(type(i),"   ",i)
        temp = poi[poi['country'] == i]
        data['country'] = i
        data['count'] = int(temp['country'].count())
        # print(data)
        graph_data.append(data)
    # print(graph_data)
    return jsonify(graph_data)


if __name__ == '__main__':
    # main()
    app.run(host="0.0.0.0",port=5000, debug=True)