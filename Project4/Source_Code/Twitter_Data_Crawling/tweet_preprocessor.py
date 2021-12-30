import demoji, re, datetime
import preprocessor


demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess_poi_tweets(cls, tweet,location):
        tweets_data = {'id':tweet.id, 
            'poi_name': tweet.user.screen_name,
            'poi_id': tweet.user.id,
            'verified': tweet.user.verified,
            'country': location,
            
            'tweet_text': tweet.full_text,
            'tweet_lang': tweet.lang,
            'text_en':update_text_xx(tweet,'en'),
             'text_hi':update_text_xx(tweet,'hi'),
             'text_es':update_text_xx(tweet,'es'),
            
            'hashtags':_get_entities(tweet, 'hashtags'),
            'mentions': _get_entities(tweet, 'mentions'),
            'tweet_urls': _get_entities(tweet, 'urls'),
            'tweet_emoticons':_text_cleaner(tweet.full_text)[1],
            'tweet_date': _get_tweet_date(tweet.created_at).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'geolocation': tweet.geo,
            }
      

        for k,v in tweets_data.items():
          tweets_data={k: v for k, v in tweets_data.items() if v}
        return tweets_data
    @classmethod
    def preprocess_keyword_tweets(cls, tweet,location):
        tweets_data = {'id':tweet.id, 
            'verified':tweet.user.verified ,
            'country': location,
            
            'tweet_text': tweet.full_text,
            'tweet_lang': tweet.lang,
            'text_en':update_text_xx(tweet,'en'),
             'text_hi':update_text_xx(tweet,'hi'),
             'text_es':update_text_xx(tweet,'es'),
            
            'hashtags':_get_entities(tweet, 'hashtags'),
            'mentions': _get_entities(tweet, 'mentions'),
            'tweet_urls': _get_entities(tweet, 'urls'),
            'tweet_emoticons':_text_cleaner(tweet.full_text)[1],
            'tweet_date': _get_tweet_date(tweet.created_at).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'geolocation': tweet.geo,
            }
      

        for k,v in tweets_data.items():
          tweets_data={k: v for k, v in tweets_data.items() if v}
        return tweets_data
        ##raise NotImplementedError

    @classmethod
    def preprocess_replies_tweets(cls, tweet,location):
        tweets_data = {'id':tweet.id, 
            'verified': tweet.user.verified,
            'country': location,
            'replied_to_tweet_id': tweet.in_reply_to_status_id,
            'replied_to_user_id': tweet.in_reply_to_user_id,
            'reply_text': _text_cleaner(tweet.full_text)[0],
            'tweet_text': _text_cleaner(tweet.full_text)[0],
            'tweet_lang': tweet.lang,
            'text_en':update_text_xx(tweet,'en'),
            'text_hi':update_text_xx(tweet,'hi'),
            'text_es':update_text_xx(tweet,'es'),
            
            'hashtags':_get_entities(tweet, 'hashtags'),
            'mentions': _get_entities(tweet, 'mentions'),
            'tweet_urls': _get_entities(tweet, 'urls'),
            'tweet_emoticons':_text_cleaner(tweet.full_text)[1],
            'tweet_date': _get_tweet_date(tweet.created_at).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'geolocation': tweet.geo,
            }
      

        for k,v in tweets_data.items():
          tweets_data={k: v for k, v in tweets_data.items() if v}
        return tweets_data

def update_verified(tweet):
  if hasattr(tweet,'verified'):
    return tweet.user.verified
  else:
    return "False"


def update_text_xx(tweet,language):
  if (tweet.lang==language):
    return _text_cleaner(tweet.full_text)[0]
  else:
    return ""

  
        


def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet.entities['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet.entities['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet.entities['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
    return _hour_rounder(tweet_date)


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))
