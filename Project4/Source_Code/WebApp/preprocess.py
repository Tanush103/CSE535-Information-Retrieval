import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
import urllib.parse
from guess_language import guess_language

class Preprocessor:
    def __init__(self):
        self.en = set(stopwords.words('english'))   #english
        self.es = set(stopwords.words('spanish'))  #spanish
        self.ps = PorterStemmer()

    def get_query(self, query):
        #query = "Бильд. Внутренний документ говорит, что Германия примет 1,5 млн беженцев в этом году"  #remove
        # query = "(Russia's intervention in Syria)"
        if query[-1] == '\n':
            query=query[:-1]
        lang = guess_language(query)
        # print(query, lang)
        # if lang == 'UNKNOWN':
        #     lang = 'en'
        query = self.tokenizer(query, lang)
        # print(query)
        query = query.replace(':',r'\:')
        # query = '('+query+')'
        # print(query)
        query = urllib.parse.quote(query)
        # final_search_query = 'text_'+lang+':'+query
        # final_search_query = 'text_en:'+query+
        return query

    def tokenizer(self, query, lang):
        #query = query.lower() #now the entire query is in lower case
        query = query.split(" ")
        if lang == 'es' or lang == 'en':
            sw = eval("self."+lang)
            query = [token for token in query if token not in sw]
        stem_text = []
        ps = PorterStemmer()
        # if lang=='en':
        for token in query:
            stem_text.append(ps.stem(token, to_lowercase=True))
        query = " ".join(stem_text)
        # query = query.replace(':',r'\:')
        return query