# main.py
# Dan Tablac: 59871000
# Anthony Esmeralda: [ID]

# Just testing that the program can go through all the folders in the directory
# and print the url found in each json file in each folder
# 
# We'll need to use the data['content'] for the index instead.

import os
import json

def access_json_files():
    ''' Access each domain folder and their respected json files. Prints the url in the json obj '''
    # directory concept: https://realpython.com/working-with-files-in-python/#listing-all-files-in-a-directory
    # json concept: https://www.geeksforgeeks.org/read-json-file-using-python/

    root = '../DEV'                 # 'DEV' directory contains domains (extract developer.zip first)
    directory = os.listdir(root)    # list containing each domain in 'DEV'
    for domain in directory:
        print('----------{}----------'.format(domain))  # just for showing which urls belong to what
        if os.path.isdir(os.path.join(root, domain)):  # Only get folders. Filters out some hidden files
            sub_dir = '{}/{}'.format(root,domain)           # Domain within root
            pages = os.listdir(sub_dir)                     # list json files/'pages' in domain
            for page in pages:
                json_file_location = sub_dir + '/{}'.format(page) # location of json file
                file = open(json_file_location, 'r')              # open JSON file
                data = json.load(file)                            # JSON object becomes dict
                file.close()
                print(data['url'])

if __name__ == '__main__':
    access_json_files()
    