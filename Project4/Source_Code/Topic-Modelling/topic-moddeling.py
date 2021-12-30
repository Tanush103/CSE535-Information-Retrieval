import pandas as pd
replies=pd.read_excel('keywords_sa_updated.xlsx')

replies.dropna(subset=['tweet_text'], inplace = True)
replies.reset_index(drop=True, inplace=True)

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(analyzer='word',       
                             min_df=3,                        # minimum required occurences of a word 
                             stop_words='english',             # remove stop words
                             lowercase=True,                   # convert all words to lowercase
                             token_pattern='[a-zA-Z0-9]{3,}',  # num chars > 3
                             max_features=5000,             # max number of unique words. Build a vocabulary that only consider the top max_features ordered by term frequency across the corpus
                            )
data_vectorized = vectorizer.fit_transform(replies['tweet_text'])

lda_model = LatentDirichletAllocation(n_components=15, # Number of topics
                                      learning_method='online',
                                      random_state=0,       
                                      n_jobs = -1  # Use all available CPUs
                                     )
lda_output = lda_model.fit_transform(data_vectorized)

import numpy as np

# Show top 20 keywords for each topic
def show_topics(vectorizer=vectorizer, lda_model=lda_model, n_words=5):
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
    return topic_keywords

topic_keywords = show_topics(vectorizer=vectorizer, lda_model=lda_model, n_words=10)        

# Topic - Keywords Dataframe
df_topic_keywords = pd.DataFrame(topic_keywords)
df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
df_topic_keywords['id'] = [i for i in range(df_topic_keywords.shape[0])]

Topics_theme = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
df_topic_keywords['topic_theme'] = Topics_theme

df_topic_keywords.set_index('topic_theme', inplace=True)

# Create Document - Topic Matrix
lda_output = lda_model.transform(data_vectorized)

# column names
topicnames = df_topic_keywords.T.columns
topicnames = ["Topic" + str(i) for i in range(15)]

# index names
docnames = ["Tweet" + str(i) for i in range(len(replies))]

id=[i for i in range(len(replies))]

# Make the pandas dataframe
df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=[topicnames], index=docnames)

# Get dominant topic for each document
dominant_topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic['dominant_topic'] = dominant_topic

df_document_topic.reset_index(inplace=True)
df_sent_topic= pd.merge(replies, df_document_topic, left_index=True, right_index=True)
#df_sent_topic.drop('index', axis=1, inplace=True)

df_sent_topic['dominanttopic']=0
for i in range(0,len(df_sent_topic)):
  df_sent_topic['dominanttopic'][i]=df_sent_topic[('dominant_topic',)][i]

df=df_sent_topic.merge(df_topic_keywords,left_on='dominanttopic',right_on='id', how='left')

df['words']=''
for i in range(0,len(df)):
  df['words'][i]=df['Word 0'][i]+','+df['Word 1'][i]+','+df['Word 2'][i]+','+df['Word 3'][i]+','+df['Word 4'][i]+','+df['Word 5'][i]+','+df['Word 6'][i]+','+df['Word 7'][i]+','+df['Word 8'][i]+','+df['Word 9'][i]


df.to_excel('keywords_with_topic.xlsx')