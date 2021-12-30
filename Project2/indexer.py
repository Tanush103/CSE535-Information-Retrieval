'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from typing import Counter
from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.skip_index=OrderedDict({})
        self.linkedlist=LinkedList()

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def get_skip_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.skip_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        
        for t in tokenized_document:
            self.add_to_index(t, doc_id)
            
        ##return index

    def add_to_index(self, term_, doc_id_):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
       
        
        index=self.get_index()
        
       
        if term_ not in list(self.inverted_index.keys()):
          
          self.inverted_index[term_]=LinkedList()

        index[term_].insert_at_end(int(doc_id_))
        #index[term_].removeDuplicates()
        return self.inverted_index        ##raise NotImplementedError

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        skip_pointers=[]
        
        index=self.get_index()
        
        #n_skips,length_between_skips= self.linkedlist.add_skip_connections()
        for k in (self.inverted_index.keys()):
            index_list=[]
            index_list=self.inverted_index[k].traverse_list()
            skip_pointers=self.inverted_index[k].traverse_skips(len(index_list))
            self.skip_index[k]=LinkedList()
            for i in skip_pointers:
                self.skip_index[k].insert_at_end(i)
        return self.skip_index 

    def calculate_tf_idf(self,df,tf,totaldocs):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        idf=totaldocs/df
        tfidf=tf*idf
        return tfidf
