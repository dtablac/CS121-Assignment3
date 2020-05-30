import ast
import json
import time
import threading
import re
import string
from nltk.stem import PorterStemmer
from cosine_similarity import *
from flask import Flask, request, render_template

app = Flask(__name__)

def get_postings(token):
    with open('index/index.txt','r') as index:
        try:
            fp = index_of_index[token]
            index.seek(fp)
            line = ast.literal_eval(index.readline())
            if token == line[0]:
                values[token] = list(line[1].items())
                tf_idf[token] = line[1]    # dict of tokens as keys, dicts as values (doc_id: tf-idf)
        except KeyError: # index_of_index key error
            return []

def create_big_dict(tokens, doc_ids):
    if doc_ids == None:
        return None
    big_dict = {}
    for token in tokens:
        big_dict[token] = {}
        for doc_id in doc_ids:
            big_dict[token][doc_id] = tf_idf[token][doc_id]
    return big_dict
        

def intersect_doc_ids():
    posting_lengths = {}
    for key in values.keys():
        posting_lengths[key] = len(values[key])
    posting_lengths = sorted(list(posting_lengths.items()), key=lambda item: item[1])       # sort the posting lengths by smallest to greatest.

    if len(posting_lengths) > 0:
        token = posting_lengths[0][0]                                  # get the first token in our posting length since format is of [(t1, l1),(t2, l2),(t3, l3)]
        intersected = [item[0] for item in values[ token ]]             # value[token] = (docid, tf-idf); so we want to get item[0] cause we want doc id.
        if (len(posting_lengths) > 1):                                  # if there are more tokens in posting length then...
            for posting in posting_lengths[1:]:                          # do every token except the first one
                temp_list = []                                           # create a temp list.                       
                token = posting[0]                                       # store the new token to be found
                temp_list = [item[0] for item in values[token]]          # our temp list will have their doc_ids
                intersected = list(set(temp_list) & set(intersected))
        return intersected
    else:
        return None

def show_urls(scores: dict):
    ''' Prints the top 5 urls from the search (AND only) '''
    global values, doc_ids
    if scores == None or len(scores) == 0:
        return None
    big_list = sorted(list(scores.items()), key=lambda item: item[1])
    results = []
    for items in big_list:
        url = doc_ids[str(items[0])]
        if '#' not in url:
            results.append(doc_ids[str(items[0])])
    return results[:5]

### -------------------------- Helper Functions -------------------------- ###

def _list_doc_ids(postings: list):
    ''' Get doc_ids [x,x2,...] from posting list [[x,y],[x2,y2],...] '''
    doc_ids = []
    for posting in postings:
        doc_ids.append(posting[0])
    return doc_ids

def _render_response(result: list):
    ''' Formats top 5 urls for page render '''

    # --- Format the urls as html list --- #
    if result == None:
        html_result = "<h3>No search results found</h3>"
    else:
        html_result = '<div class="fade"><ol class="results">'
        for i in range(len(result)):
            html_result += '<li><a href={}>{}</a></li>'.format(result[i], result[i])
        html_result += '</ol></div>'

    # --- Rewrite html template --- # (index.html includes results.html)
    result_file = open('templates/results.html','w')
    result_file.write(html_result)
    result_file.close()

### -------------------------- API Endpoints -------------------------- ###

# --- Home page loads on first visit or home url entered in browser --- #
@app.route('/')
def main():
    result_file = open('templates/results.html','w')
    result_file.write('')
    result_file.close()
    return render_template('index.html')

# --- Flask routes POST requests made from index.html --- #
@app.route('/', methods=['POST'])
def run_search():
    user_query = request.form['search']    # Contents of search bar

    # --- Do stuff with search query --- #
    search_query = user_query.lower()
    search_query = search_query.translate(str.maketrans(string.punctuation,' ' * len(string.punctuation)))
    search_query = search_query.split()
    search_query = [ps.stem(item) for item in search_query]

    start_time = time.time()
    start = 0

    if len(search_query) == 0:
        _render_response(None)
    else: 
        query_scores = calculate_query_scores(search_query)
        values.clear()
        tf_idf.clear()

        for word in search_query:

            get_postings(word)

        big_dict = create_big_dict(search_query, intersect_doc_ids())
        scores = get_cosine_similarity_list(query_scores,big_dict)

        # --- Update 'results.html' template with urls found --- #
        _render_response(show_urls(scores))

    end_time = time.time()
    timer = (end_time - start_time)
    runtime = timer * 1000
    timestamp = 'Retrieved in {} ms.'.format(runtime)

    # --- Render results (check index.html), query, and time --- #
    return render_template('index.html', query=user_query, time=timestamp)

### ---------- Main ---------- ###

if __name__ == '__main__':
    # --- Load index of tokens mapped to the file's line. --- # 
    #     This prevents loading entire index to memory.       #
    values = {}
    tf_idf = {}

    ps = PorterStemmer()    # Stems tokens in user query

    with open('index/index_for_index.txt','r') as index_index:
        index_of_index = json.load(index_index) 

    doc_ids_file = open('index/doc-ids.txt','r')    # Load doc-ids for URL ref
    doc_ids = json.load(doc_ids_file)
    doc_ids_file.close()

    app.run(debug=True)
