# -*- coding: utf-8 -*-


import json
# if you are using python 3, you should 
#import urllib.request 
import urllib.request as urllib2
#import urllib2
import re
from urllib.parse import quote
import os.path

models=['BM25', 'VSM'] 
# change the url according to your own corename and query

inquery='test-queries.txt'
#outfn = 'input_bm25.txt'


with open(inquery,"r",encoding="utf-8") as f :
    lines=f.readlines()
    
for line in lines:
    #line.replace("\n", "")
    line=line[:-1]
    #arr=line.split("\t")
    
    
    query_text=line[4:]
    #hashtags = re.findall(r"#(\w+)", query_text)
    #retweets = re.findall(r"@(\w+)", query_text)
    query = query_text.replace(":", "\:")
    query="(" + query + ")"
    query=quote(query)
    for model in models:
        inurl = 'http://ec2-3-15-200-112.us-east-2.compute.amazonaws.com:8983/solr/'+model+'/select?q=text_en:{0}%20OR%20text_de:{0}%20OR%20text_ru:{0}&fl=id%2Cscore&wt=json&indent=true&rows=20'.format(query)
    # change query id and model name accordingly
        qid=line[0:3]
    #qid =query_id
    #IRModel='bm25' #either bm25 or vsm
        if not os.path.exists(model):
            os.makedirs(model)

        output_file_name = qid.lstrip("0")+".txt"
        output_file = os.path.join(model, output_file_name)


        outf = open(output_file, 'a+')
        data = urllib2.urlopen(inurl)
    # if you're using python 3, you should use
    # data = urllib.request.urlopen(inurl)

        docs = json.load(data)['response']['docs']
        # the ranking should start from 1 and increase
        rank = 1
        for doc in docs:
            outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + model.lower() + '\n')
            rank += 1
outf.close()
