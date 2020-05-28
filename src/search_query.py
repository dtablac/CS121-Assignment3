import ast
import json
import time
import threading
from nltk.stem import PorterStemmer
from flask import Flask, request, render_template

app = Flask(__name__)

def get_postings(token):
    ''' takes a token, and will try to find that token's inverted index postings in the index_postings file '''
    ''' we open a new fp everytime because seek(0,0) may not be thread friendly '''
    with open('merges/merge3.txt','r') as index:
        try:
            fp = index_of_index[token]
            index.seek(fp)
            line = ast.literal_eval(index.readline())
            if token == line[0]:
                values[token] = sorted(list(line[1].items()), reverse=True, key=lambda item: item[1])
        except KeyError: # index_of_index key error
            return []

def create_threads(query_list):
    ''' Creates threads for each individual token in the query '''
    threads = []
    for query in query_list:
        threads.append(threading.Thread(target=get_postings, args=(query,)))
    return threads

def _list_doc_ids(postings: list):
    ''' Get doc_ids [x,x2,...] from posting list [[x,y],[x2,y2],...] '''
    doc_ids = []
    for posting in postings:
        doc_ids.append(posting[0])
    return doc_ids


def show_urls():
    ''' Prints the top 5 urls from the search (AND only) '''
    global values, doc_ids

    postings = []
    # --- Get all posting lists for each token. Store in postings list --- #
    for token in values:
        postings.append(_list_doc_ids(values[token]))
        
    try:
        # --- AND documents that query tokens appear in --- #
        intersected = postings[0]
        if (len(postings) > 1):
            for posting in postings[1:]:
                intersected = set(intersected).intersection(posting)
        result_list = list(intersected)[:5]
        # --- Print urls --- #
        if len(result_list) == 0:
            return None
        else:
            result = []
            for item in result_list:
                result.append(doc_ids[str(item)])
            return result

    except IndexError:
        # --- If no URLs from retrieval and/or intersection --- #
        return None

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

    # --- Unlike React, rewrite html template itself LOL --- # (index.html includes results.html)
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
    search_query = search_query.split()
    search_query = [ps.stem(item) for item in search_query]
    values.clear()


    # threads = create_threads(search_query)
    # start = time.time()
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()

    start = 0

    for word in search_query:
        start_temp_time = time.time()
        get_postings(word)
        end_temp_time = time.time()
        start += (end_temp_time - start_temp_time)

    runtime = start * 1000

    # --- Update 'results.html' template with urls found --- #
    _render_response(show_urls())

    timestamp = 'Retrieved in {} ms.'.format(runtime)

    # --- Render results (check index.html), query, and time --- #
    return render_template('index.html', query=user_query, time=timestamp)

### ---------- Main ---------- ###

if __name__ == '__main__':
    # --- Load index of tokens mapped to the file's line. --- # 
    #     This prevents loading entire index to memory.       #
    values = {}

    ps = PorterStemmer()    # Stems tokens in user query

    with open('index_for_index.txt','r') as index_index:
        index_of_index = json.load(index_index) 

    doc_ids_file = open('doc-ids.txt','r')    # Load doc-ids for URL ref
    doc_ids = json.load(doc_ids_file)
    doc_ids_file.close()

    app.run(debug=True)
