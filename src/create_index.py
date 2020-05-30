# main.py
# Dan Tablac: 59871000
# Anthony Esmeralda: 45111521

import os
import sys
import json
import re
import sys
import string
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from frequency import computeWordFrequencies
from merger import merge_indexes
from tf_idf import compute_tf_idf
from normalize import normalize
from index_for_index import create_index_for_index

# ---------- Index Implementation ---------- #

def _assign_doc_id(document_url: str):
    ''' Assign document id to a url. '''
    global doc_ids
    global doc_id_counter

    doc_ids[doc_id_counter] = document_url   # map current doc_id to url
    returning_doc_id = doc_id_counter    # temp store of currnet doc_id before incrementing (to be used by next document)
    doc_id_counter += 1
    return returning_doc_id

def _add_posting(freq_list: dict, doc_id: int):
    ''' For each token in the frequency list, add its term frequency in a document to the index '''
    global inverted_index
    for token, frequency in freq_list.items():
        if token not in inverted_index:
            seen.add(token)
            inverted_index[token] = {}
        inverted_index[token][doc_id] = frequency

def _offload_index(offload_counter):
    ''' Offload index to a partial index and clear in-memory index. Each item in partial is written on a new line '''
    with open("partials/partial_index" + str(offload_counter) + ".txt", 'w') as output:
        sorted_inverted_index = sorted(inverted_index.items(), key= lambda kv: kv[0])
        for item in sorted_inverted_index:
            output.write(str(item) + '\n')
        inverted_index.clear()

def _tokenize(token_string) -> list:
    more_restrictful_alphanum = re.compile(r'^[0-9A-Za-z]*$')               # alphanum() allows non-english characters
    tokens = []
    token_string = token_string.translate(str.maketrans(string.punctuation,' ' * len(string.punctuation)))   # treat all punctuation's as spaces.
    token_string = token_string.split()                                               # convert our string into a list of tokens.
    for token in token_string:                                                   # iterate through our raw tokens
        if len(token) >= 2 and more_restrictful_alphanum.match(token):      # only add the "token" to our tokens list if
            tokens.append(token.lower())                                    # it satisfies our constraint
    return tokens      

def access_json_files(root):
    ''' Access each domain folder and their respected json files. '''
    # directory concept: https://realpython.com/working-with-files-in-python/#listing-all-files-in-a-directory
    # json concept: https://www.geeksforgeeks.org/read-json-file-using-python/
    # re and BeautifulSoup documentations referenced

    corpus = os.listdir(root)    # list containing each domain in 'DEV'
    
    # --- Check each domain (folder) --- #
    doc_counter = 0             # Counts how many documents we've indexed in this partial
    offload_counter = 1     # racks how many times index has been offloaded to a partial, included in partial name

    for domain in corpus:
        if os.path.isdir(os.path.join(root, domain)):  # Only get folders. Ignores .DS_Store in mac.
            print('Indexing: {}'.format(domain))  # Prints domain currently being indexed.
            sub_dir = '{}/{}'.format(root,domain)           # Path to domain within root.
            pages = os.listdir(sub_dir)                     # List pages in current domain.

            for page in pages:
                doc_counter += 1
                json_file_location = sub_dir + '/{}'.format(page)   # Path to page
                file = open(json_file_location, 'r')                # Open JSON file
                data = json.load(file)                              # JSON object becomes dict
                file.close()

                # --- Tokenize page, add postings of tokens in this doc to the index --- #
                id = _assign_doc_id(data['url'])                      # Give a unique doc_id to our url.
                soup = BeautifulSoup(data['content'], 'html.parser')  # Process html for parsing.
                token_string = soup.get_text()                        # Get all text from processed html
                tokens = _tokenize(token_string)                      # Tokenize the text.
                tokens = [ps.stem(token) for token in tokens]         # Stem each token.
                freq_list = computeWordFrequencies(tokens)            # Compute each token frequency in this page.
                _add_posting(freq_list,id)                            # Add all token frequencies from this page to the index

                # --- Offload to a partial index every 15,000 pages --- #
                if (doc_counter % 15000) == 0:
                    print("15,000 pages reached.")
                    print("Offloading into partial_index{}.txt ...".format(offload_counter))
                    _offload_index(offload_counter)
                    offload_counter += 1
                    print("Done.")
                    print("Continuing...")

    ''' Offload the rest of the index after the last document is indexed. '''
    if len(inverted_index) != 0:  # If some documents left in in-memory index, offload them.
        print("Offloading remaining into partial_index{}.txt ...".format(offload_counter))
        _offload_index(offload_counter)
        print('Done.')

if __name__ == '__main__':
    # ---------- Initial Variables ---------- #
    doc_id_counter = 1    # Unique doc_id counter
    seen = set()
    inverted_index = dict()      # { token: { doc_id: tf } }
    doc_ids = dict()    # { doc_id: url }
    ps = PorterStemmer()   
    # -------------------------------------- #

    print('Crawling through documents in the collection...')
    
    access_json_files('../DEV') # 'DEV' directory contains domains (extract developer.zip first)

    print('Done accessing collection.')

    N = doc_id_counter - 1    # Number of documents
    unique_tokens = len(seen)

    print('Number of documents: {}'.format(N))
    print('Unique tokens: {}'.format(unique_tokens))

    print('Writing doc_ids to txt...')
    with open('index/doc-ids.txt','w') as output1:
        json.dump(doc_ids, output1)
    print('Done.')

    # ----- Merge all partial indexes into 'merge3.txt'  ----- #

    print('Merging partial index files...')

    piOne = open('partials/partial_index1.txt', 'r')
    piTwo = open('partials/partial_index2.txt', 'r')
    piThree = open('partials/partial_index3.txt', 'r')
    piFour = open('partials/partial_index4.txt', 'r')

    merge_indexes(1,piOne,piTwo)
    pmi = open('merges/merge1.txt','r')
    merge_indexes(2,pmi,piThree)
    pmi2 = open('merges/merge2.txt','r')
    merge_indexes(3,pmi2,piFour)

    piOne.close()
    piTwo.close()
    piThree.close()
    piFour.close()
    pmi.close()
    pmi2.close()

    print('Done.')

    # ----- merge3.txt (tentative index is created) ----- # 

    ### ----- Change term frequencies in tentative index to idf----- ###

    # ----- Calculate tf-idf of each token, for each document in their posting list. ----- #
    # ----- A new index is created under the name 'temp_final_index.txt' ----- #
    print('Converting term frequency scores to tf-idf...')
    compute_tf_idf(N)
    print('Done.')

    # ----- Index the new tf-idf computed index, still need to normalize those scores ----- #
    i = create_index_for_index('index/temp_index.txt')
    with open('index/index_for_index.txt','w') as index_index:
        json.dump(i, index_index)
    
    # ----- Normalize tf-idfs and create final 'index.txt'----- #
    with open('index/index_for_index.txt','r') as index_index:
        index_for_index = json.load(index_index)
    print('Normalizing tf-idf scores...')
    normalize(index_for_index)
    print('Done.')

    # delete temp_index.txt after final index.txt is created?

    # ---- Index the final, normalized, index. ----- #
    i = create_index_for_index('index/index.txt')
    with open('index/index_for_index.txt','w') as index_index:
        json.dump(i, index_index)

    print("Final index written to 'index/index.txt.'")
    print('Index created.')