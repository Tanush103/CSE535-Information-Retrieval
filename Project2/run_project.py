'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, p1, p2):
        answer = LinkedList()
        cur1 = p1.start_node
        cur2 = p2.start_node
        cmp = 0
        while cur1 is not None and cur2 is not None:
            if cur1.value == cur2.value:
                answer.insert_at_end(int(cur1.value))
                cur1 = cur1.next
                cur2 = cur2.next
            elif cur1.value < cur2.value:
                cur1 = cur1.next
            else:
                cur2 = cur2.next
            cmp +=1
        return answer, cmp

    def _daat_and(self,query_list):
        """ Implement e DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        results = []
        sortedlist=[]
        num_comparisons = 0

        daat_temp_dict = {}
    
    # Below code segment is for sorting the Dictionary according to the frequency of terms and saving the terms in ascending order in 'words' list
        d ={}
        index=self.indexer.get_index()
        
        for word in query_list:
            d[word] = len(index[word].traverse_list())
        a = sorted(d.items(), key=lambda x: x[1])
        query_list.clear()
        for c in a:
            query_list.append(c[0])
        #print(len(query_list))
        
        # Main meat of the daatAND function
        if len(query_list) == 0:
            num_comparisons = 0
            results.append(None.traverse_list())
            

        elif len(query_list) == 1:
            num_comparisons = 0
            results.append(index[query_list[0]].traverse_list())
        elif len(query_list) == 2:
            p1 = query_list.pop(0)
            p2 = query_list.pop(0)
            
            intermediate,cmp = self._merge(index[p1],index[p2])
            num_comparisons = cmp
            #print(intermediate.traverse_list())
            #print(num_comparisons)
            results.append(intermediate.traverse_list())
        else:
            p1 = query_list.pop(0)
            #p1 = words.pop(0)
            p2 = index[query_list.pop(0)]
            while True:
                intermediate,cmp = self._merge(index[p1],p2)
                
                #cmp= _merge(term_list[p1],term_list[p2])[1]
                num_comparisons += cmp
                if(len(query_list) == 0):
                    p2 = intermediate
                    break
                p1 = query_list.pop(0)
                p2 = intermediate
            results.append(p2.traverse_list())

        
        # print(num_comparisons)
        #sortedlist=list(set(results[0]))
        return results[0],num_comparisons 

    
    def _get_postings(self,query):
    
        index=self.indexer.get_index()
        #index1=OrderedDict({})
        #print(index)
        postings_list=[]
        if query in list(index.keys()):
            postings_list=index[query].traverse_list()
            #index1[query]=index[query]
        return list(sorted(set(postings_list)))

    def _get_skip_postings(self,query):
    
        index=self.indexer.get_index()
        #index1=OrderedDict({})
        #print(index)
        postings_list=[]
        if query in list(index.keys()):
            postings_list=index[query].traverse_list()
            #index1[query]=index[query]
        return list(sorted(set(postings_list)))        

    def _get_postings(self,query):
    
        index=self.indexer.get_index()
        #index1=OrderedDict({})
        #print(index)
        postings_list=[]
        if query in list(index.keys()):
            postings_list=index[query].traverse_list()
            #index1[query]=index[query]
        return list(sorted(set(postings_list)))

    def _get_skip_postings(self,query):
    
        index=self.indexer.get_skip_index()
        #index1=OrderedDict({})
        #print(index)
        postings_list=[]
        if query in list(index.keys()):
            postings_list=index[query].traverse_list()
            #index1[query]=index[query]
        return list(sorted(set(postings_list)))        

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r',encoding="utf-8") as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
                
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        ##self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            
            tokenized_query = self.preprocessor.tokenizer(query)
            
           
            input_term_arr = tokenized_query  # Tokenized query. To be implemented.
            
            for term in input_term_arr:
                postings, skip_postings = None, None
                
                postings=self._get_postings(term)
                    #postings.append([inverted_index[qterm]['docids'].postings(),inverted_index[qterm]['dfreq']])
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""
                skip_postings=self._get_skip_postings(term)

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            #index=self.indexer.get_index()
            and_op_no_skip,and_comparisons_no_skip=self._daat_and(input_term_arr)
            #and_op_no_score_skip, and_results_cnt_skip=self._daat_and_skip(input_term_arr)
            #and_op_no_skip,_comparisons_no_skip=self._daat_and(input_term_arr)
            #and_op_no_score_no_skip=self._daat_and(input_term_arr,index)['results']
            #and_results_cnt_no_skip=self._daat_and(input_term_arr,index)['num_docs']
            #and_comparisons_no_skip=self._daat_and(input_term_arr,index)['num_comparisons']
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

            f = open("dict.txt","w")

            # write file
            f.write( str(output_dict) )

            # close file
            f.close()
        return output_dict

@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    corpus_location = "project2\data\input_corpus.txt"
    username="tanushtr"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help=".\data\input_corpus.txt",default="data\input_corpus.txt")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here",default="tanushtr")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9998)
