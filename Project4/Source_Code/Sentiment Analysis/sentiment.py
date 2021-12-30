import pandas as pd
import numpy as np
import hashlib
import pathlib
import pickle
#from textblob import TextBlob
from deep_translator import GoogleTranslator
import nltk
nltk.download("punkt")
import string
from flair.models import TextClassifier
from flair.data import Sentence
import re


sia = TextClassifier.load('en-sentiment')

news=pd.read_excel('keywords.xlsx')
news['sentiment']=0.0

def sentiment_analysis(text):
    sentence=Sentence(text)
    sia.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
            label = str(sentence.labels[0]).split()[1]
            string = re.sub("[()]","", label)
            number=float(string)
            return number
            


    elif "NEGATIVE" in str(score):
          label = str(sentence.labels[0]).split()[1]
          string = re.sub("[()]","", label)
          number=-1.0*float(string)
          return number 
    else:
          return 0


for i in range(0,len(news)):
  try:
    news['sentiment'][i]=sentiment_analysis(str(GoogleTranslator(source='auto', target='en').translate(news['tweet_text'][i])).lower())
    print(i)
  except:
    news['sentiment'][i]=0
news.to_excel('keywords_sa_updated.xlsx',index=False)