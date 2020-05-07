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
from PartA import computeWordFrequencies

# ---------- Global Variables ---------- #

doc_id_counter = 1    # Unique doc_id counter

inverted_index = dict()      # Store word(str) -> posting(list) pairings.

doc_ids = dict()    # Store doc_id -> doc_name pairings

ps = PorterStemmer()
# ---------- Index Implementation ---------- #

# store postings in python STL list as [ [doc_id, token_frequency], ... ]

#class Posting:
#    def __init__(self, id, score):
#        self.id = id                # document id that token was found (from doc_ids)
#        self.score = score          # "tf_ifd score"
#
#    def __repr__(self):
#        return str('(doc_id: {}, score: {})'.format(self.id, self.score))

# ------------------------------------------ #

def _assign_doc_id(document):
    ''' Assign document id to a document. '''
    global doc_ids
    global doc_id_counter

    doc_ids[doc_id_counter] = document
    returning_doc_id = doc_id_counter    # temp store of original doc_id before incrementing
    doc_id_counter += 1
    return returning_doc_id

#def _add_posting(token, id):
#    ''' Adds/updates a posting, of the token's occurence in a document (id), in the inverted index '''
#    global inverted_index
#    token2 = token.lower()                                  # O(w)
#    posting_updated = False
#    try:
#        for posting in inverted_index[token2]:              # O(b)
#            if posting.id == id:
#                posting.score += 1
#                posting_updated = True
#                break
#        if posting_updated == False:
#            inverted_index[token2].append(Posting(id, 1))
#    except KeyError:
#        inverted_index[token2] = []
#        inverted_index[token2].append(Posting(id, 1))

def _add_posting(freq_list, id):
    global inverted_index
    for key, value in freq_list.items():
        if key not in inverted_index:
            inverted_index[key] = []
            inverted_index[key].append([id,value])
        else:
            inverted_index[key].append([id,value])
    
def access_json_files(root):
    ''' Access each domain folder and their respected json files. '''
    # directory concept: https://realpython.com/working-with-files-in-python/#listing-all-files-in-a-directory
    # json concept: https://www.geeksforgeeks.org/read-json-file-using-python/
    # re and BeautifulSoup documentations referenced

    corpus = os.listdir(root)    # list containing each domain in 'DEV'
    
    # --- Check each domain (folder) --- #
    for domain in corpus:
        if os.path.isdir(os.path.join(root, domain)):  # Only get folders. Ignores .DS_Store in mac
            print('----------{}----------'.format(domain))  # just for showing which urls belong to what
            
            sub_dir = '{}/{}'.format(root,domain)           # Path to domain within root
            pages = os.listdir(sub_dir)                     # list json files, or 'pages', in domain
            for page in pages:
                id = _assign_doc_id(page)                         # give json file a unique doc_id
                json_file_location = sub_dir + '/{}'.format(page) # Path to page

                file = open(json_file_location, 'r')              # open JSON file
                data = json.load(file)                            # JSON object becomes dict
                file.close()

                # --- Do Stuff with the data --- #
                soup = BeautifulSoup(data['content'], 'html.parser')
                token_string = soup.get_text()
                tokens = tokenize(token_string)
                tokens = [ps.stem(token) for token in tokens]
                freq_list = computeWordFrequencies(tokens)
                _add_posting(freq_list,id)

# ------------------------------------------ #
# --------------- tokenizing-----------------#

def tokenize(token_string) -> list:
    more_restrictful_alphanum = re.compile(r'^[0-9A-Za-z]*$')               # alphanum() allows non-english characters
    tokens = []
    token_string = token_string.translate(str.maketrans(string.punctuation,' ' * len(string.punctuation)))   # treat all punctuation's as spaces.
    token_string = token_string.split()                                               # convert our string into a list of tokens.
    for token in token_string:                                                   # iterate through our raw tokens
        if len(token) >= 2 and more_restrictful_alphanum.match(token):      # only add the "token" to our tokens list if
            tokens.append(token.lower())                                    # it satisfies our constraint
    return tokens      

if __name__ == '__main__':
    access_json_files('../DEV') # 'DEV' directory contains domains (extract developer.zip first)

    print('Writing doc_ids to txt...')
    with open('doc-ids.txt','w') as output1:
        json.dump(doc_ids, output1)
    print('Done.')

    print('Writing index to txt...')
    with open('index.txt','w') as output2:
        json.dump(inverted_index, output2)
    print('Done.')

    print('Number of documents: {}'.format(doc_id_counter-1))
    print('Unique tokens: {}'.format(len(list(inverted_index.keys()))))