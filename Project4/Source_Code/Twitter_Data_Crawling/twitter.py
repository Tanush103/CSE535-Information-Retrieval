import tweepy
import json
import pandas as pd
import numpy as np


class Twitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler("lnp4tNxwWKta2D6N4rTLJ6ebX", "SAc2ps3es51lwfF7LIQD8L4EqbXUT8A4IZFfliAjnXChsTJn8t")
        self.auth.set_access_token("1432401848527466497-1u5kfYxeQ4c1kJp2a9TvoH51CkrFUZ", "QCaevSZ11RZHb8vzbV0kyD1ZGJVFiH1Aw3MMF1oUV3qLV")
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        f=open("config.json", encoding='utf-8')
        self.data=json.load(f)
        
    def _meet_basic_tweet_requirements(self, tweet, lang=None):
        if (tweet.full_text.lower()).startswith("rt @"):
            return 0
        elif tweet.retweeted is True:
            return 0
        elif lang:
            if lang == tweet.lang:
                return 1
            else:
                return 0
        else:
            return 1

    def get_tweets_by_poi_screen_name(self,name,count):
        tweets_list=[]
        replies_list=[]
        
        #date_since = "2020-11-16"
        for full_tweets in tweepy.Cursor(self.api.user_timeline,screen_name=name,result_type="recent",tweet_mode="extended",timeout=999999).items(count):
          
          tweets_list.append(full_tweets)
        return tweets_list
            

        

        ##raise NotImplementedError

    def get_tweets_by_lang_and_keyword(self,count,name,language):
        tweets_list=[]
        replies_list=[]
        date_since = "2020-11-16"

        search_words=name
        for full_tweets in tweepy.Cursor(self.api.search,q=search_words, result_type='recent',since=date_since,tweet_mode="extended", timeout=999999).items(count):
          tweets_list.append(full_tweets)

        return tweets_list
        
        
           
        
    def get_replies(self,name):
        #name = 'JoeBiden'
        poi=pd.read_csv('poi.csv')
        poi.reset_index(drop=True, inplace=True)
        #is_poi =  poi['poi_name']=="MoHFW_INDIA"
        #single_poi=poi[is_poi]
        #single_poi.reset_index(drop=True, inplace=True)
        list1=[]
        for i in range(0,len(poi)):
            list1.append(str(poi['id'][i]))
        s1 = set(list1)
        #tweet_id = '1462483454218711046'
        replies=[]
        # for tweet_id in list1:
        for page in tweepy.Cursor(self.api.search,q='to:'+name, result_type='recent',tweet_mode="extended",timeout=999999).pages(500):
            for tweet in page:
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    # if (tweet.in_reply_to_status_id_str==tweet_id):
                    if (tweet.in_reply_to_status_id_str in s1):
                        replies.append(tweet)
        print(replies)
        return replies

