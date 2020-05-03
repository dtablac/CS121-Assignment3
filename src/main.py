# main.py
# Dan Tablac: 59871000
# Anthony Esmeralda: [ID]

# Just testing that the program can go through all the folders in the directory
# and print the url found in each json file in each folder
# 
# We'll need to use the data['content'] for the index instead.

import os
import json

# ---------- Global Variables ---------- #

doc_id_counter = 1    # Unique doc_id counter

index = dict()      # Store word -> posting pairings.

doc_ids = dict()    # Store doc_name -> id pairings

# ---------- Index Implementation ---------- #

class LinkedList:
    def __init__(self):
        self.head = None

class Posting:
    def __init__(self, id, score):
        self.id = id                # document id that token was found (from doc_ids)
        self.score = score          # "tf_ifd score"
        self.next = None

# ------------------------------------------ #

def assign_doc_id(document):
    ''' Assign document id to a document. '''
    global doc_ids
    global doc_id_counter

    doc_ids[document] = doc_id_counter
    doc_id_counter += 1

def access_json_files():
    ''' Access each domain folder and their respected json files. Prints the url in the json obj '''
    # directory concept: https://realpython.com/working-with-files-in-python/#listing-all-files-in-a-directory
    # json concept: https://www.geeksforgeeks.org/read-json-file-using-python/

    root = '../DEV'                 # 'DEV' directory contains domains (extract developer.zip first)
    corpus = os.listdir(root)    # list containing each domain in 'DEV'
    
    for domain in corpus:
        if os.path.isdir(os.path.join(root, domain)):  # Only get folders. Ignores .DS_Store in mac
            print('----------{}----------'.format(domain))  # just for showing which urls belong to what
            
            sub_dir = '{}/{}'.format(root,domain)           # Domain within root
            pages = os.listdir(sub_dir)                     # list json files, or 'pages', in domain
            for page in pages:
                assign_doc_id(page)                         # give json file a unique doc_id
                json_file_location = sub_dir + '/{}'.format(page) # location of json file

                file = open(json_file_location, 'r')              # open JSON file
                data = json.load(file)                            # JSON object becomes dict
                file.close()

                # --- Do Stuff with the data --- #
                #print(data['url'])

# ------------------------------------------ #

if __name__ == '__main__':
    access_json_files()
    print('Number of documents: {}'.format(doc_id_counter-1))
    