import ast
import json
import time
import threading


f = open('index_posting_location.txt','r')                        
ip_loc = json.load(f)        # load the index of tokens mapped to the file's line; so we dont load the entire index into memory
values = {}

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
    threads = []
    for query in query_list:
        threads.append(threading.Thread(target=get_postings,args=(query,)))
    return threads

if __name__ == '__main__':
    while True:
        search_query = input("Search for: ")
        search_query = search_query.split()
        values.clear()
        start = time.time()
        threads = create_threads(search_query)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print((time.time() - start) * 1000)
        ''' do something with the data '''
        # values will hold our data
