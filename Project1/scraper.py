import json
import datetime
import pandas as pd
from  twitter import Twitter
from tweet_preprocessor import TWPreprocessor
from indexer import Indexer

reply_collection_knob = False


def read_config():
    with open("config.json", encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def write_config(data):
    with open("config.json" , 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)


def save_file(data, filename):
    df = pd.DataFrame(data)
    df.to_pickle("sample_data/" + filename)



##def read_file(type, id):
    ##return pd.read_pickle(f"data/{type}_{id}.pkl")


def main():
    config = read_config()
    indexer = Indexer()
    twitter = Twitter()
    sleep_on_rate_limit=False

    pois = config["pois"]
    keywords = config["keywords"]

    for i in range(len(pois)):
        if pois[i]["finished"] == 0:
            print(f"---------- collecting tweets for poi: {pois[i]['screen_name']}")
            raw_tweets = twitter.get_tweets_by_poi_screen_name(pois[i]["screen_name"], pois[i]["count"])
           
            processed_tweets=[]
            
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess_poi_tweets(tw,pois[i]["country"]))
            
            indexer.create_documents(processed_tweets)

            
            
           
            pois[i]["finished"] = 1
            pois[i]["collected"] = len(processed_tweets)
            
            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"poi_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")

    for i in range(len(keywords)):
        if keywords[i]["finished"] == 0:
            print(f"---------- collecting tweets for keyword: {keywords[i]['name']}")
            raw_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]["count"], keywords[i]["name"], keywords[i]["lang"])
            
            processed_tweets = []
            for tw in raw_tweets:
                processed_tweets.append(TWPreprocessor.preprocess_keyword_tweets(tw,keywords[i]["country"]))
            
            indexer.create_documents(processed_tweets)

            ##raw_reply_tweets = twitter.get_tweets_by_lang_and_keyword(keywords[i]["count"], keywords[i]["name"], keywords[i]["lang"])[1]
            
            ##processed_reply_tweets = []
            
            ##for tw in raw_reply_tweets:
            ##    processed_reply_tweets.append(TWPreprocessor.preprocess_replies_tweets(tw,keywords[i]["country"]))
            
            ##indexer.create_documents(processed_reply_tweets)
            ##keywords[i]["finished"] = 1
            keywords[i]["collected"] = len(processed_tweets)

            write_config({
                "pois": pois, "keywords": keywords
            })

            save_file(processed_tweets, f"keywords_{keywords[i]['id']}.csv")
            ##save_file(processed_reply_tweets, f"replies_keywords_{keywords[i]['id']}.csv")

    #        print("------------ process complete -----------------------------------")
    
    for i in range(len(pois)):
        if pois[i]["reply_finished"] == 0:
            print(f"---------- collecting replies on poi: {pois[i]['screen_name']} tweets")
            raw_reply_tweets = twitter.get_replies(pois[i]["screen_name"])
           
            processed_reply_tweets=[]
            
            for tw in raw_reply_tweets:
                processed_reply_tweets.append(TWPreprocessor.preprocess_replies_tweets(tw,pois[i]["country"]))
            indexer.create_documents(processed_reply_tweets)

            
            
            
            pois[i]["reply_finished"] = 1
            pois[i]["collected"] =len(processed_reply_tweets)
            
            write_config({
               "pois": pois, "keywords": keywords
            })

            save_file(processed_reply_tweets, f"poi_replies_{pois[i]['id']}.pkl")
            print("------------ process complete -----------------------------------")


if __name__ == "__main__":
  main()
