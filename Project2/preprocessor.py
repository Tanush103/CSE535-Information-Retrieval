'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from tqdm import tqdm


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        pattern = re.compile(r'[^a-zA-Z0-9]')
        s = re.sub(pattern, ' ', text)
        words = []
        words1=[]
        for word in s.split():
            word = word.strip()
            words.append(word.lower())
        words1=list(set(words))
        
        
        words_without_stopwords = [w for w in words1 if not w in self.stop_words]
        new_string=""
        new_words = []
        for word in words_without_stopwords:
            new_words.append(self.ps.stem(word))
            ##new_string=(' '.join(new_words))

        return new_words