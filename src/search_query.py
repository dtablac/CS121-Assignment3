import ast
import json
import time
import threading
from nltk.stem import PorterStemmer

def get_postings(token):
    ''' takes a token, and will try to find that token's inverted index postings in the index_postings file '''
    ''' we open a new fp everytime because seek(0,0) may not be thread friendly '''

    d = open('index_postings.txt','r') 
    try:
        for i, line in enumerate(d):                            
            if i == ip_loc[token]:
                values[token] = ast.literal_eval(line)
                return 
    except:
        pass

def create_threads(query_list):
    ''' Creates threads for each individual token in the query '''
    threads = []
    for query in query_list:
        threads.append(threading.Thread(target=get_postings,args=(query,)))
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
        L = sorted(values[token], key=lambda item: item[1], reverse=True) # Sort postings by term frequency
        postings.append(_list_doc_ids(L))
        
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
    f = open('index_posting_location.txt','r')                        
    ip_loc = json.load(f)        # load the index of tokens mapped to the file's line; so we dont load the entire index into memory
    values = {}
    f.close()
    ps = PorterStemmer()
    doc_ids_file = open('doc-ids.txt','r')
    doc_ids = json.load(doc_ids_file)
    f = open("index.txt",'rb')
    test_equal = json.load(f)

    while True:
        search_query = input("Search for: ").lower()
        search_query = search_query.split()
        search_query = [ps.stem(item) for item in search_query]
        values.clear()
        start = time.time()

        '''threads = create_threads(search_query)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        '''

        for query in search_query:
            if test_equal[query] is not None:
                values[query] = test_equal[query]
            else:
                pass
            
        runtime = (time.time() - start) * 1000
        show_urls()
        print('Retrieved in {} ms.'.format(runtime))

        # values will hold our data
