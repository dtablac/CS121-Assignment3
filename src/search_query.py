import ast
import json
import time
import threading
from nltk.stem import PorterStemmer

def get_postings(token):
    ''' takes a token, and will try to find that token's inverted index postings in the index_postings file '''
    ''' we open a new fp everytime because seek(0,0) may not be thread friendly '''
    with open('merges/merge3.txt','r') as index:
        fp = index_of_index[token]
        index.seek(fp)
        line = ast.literal_eval(index.readline())
        if token == line[0]:
            values[token] = sorted(list(line[1].items()), reverse=True, key=lambda item: item[1])

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
            print('No search results were found.')
        else:
            for item in result_list:
                print(doc_ids[str(item)])

    except IndexError:
        # --- If no URLs from retrieval and/or intersection --- #
        print('No search results were found.')


if __name__ == '__main__':
    values = {}
    
    ps = PorterStemmer()
    doc_ids_file = open('doc-ids.txt','r')
    doc_ids = json.load(doc_ids_file)

    # index of index

    with open('index_for_index.txt','r') as index_index:
        index_of_index = json.load(index_index)

    while True:
        search_query = input("Search for: ").lower()
        search_query = search_query.split()
        search_query = [ps.stem(item) for item in search_query]
        values.clear()
        start = time.time()

        for word in search_query:
            get_postings(word)
            
        results = show_urls()
        runtime = (time.time() - start) * 1000
        print('Retrieved in {} ms.'.format(runtime))

        # values will hold our data
