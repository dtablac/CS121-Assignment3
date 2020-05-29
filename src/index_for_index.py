import ast
import json
"""

This program will index the complete inverted index to make for faster seeks
at query time. The function here will output an index of the index. A dict is
used to map alphanumeric characters to the file position in the index at which
posting lists are found for each token

This way, for each query term, we can jump straight it in the index.

"""

def create_index_for_index()->dict:
    index_of_index = {}
    print('Writing index for index ...')
    with open('final_index_2.txt','r') as index:
        while True:
            try:
                current_fp = index.tell()    # current file position 
                line = ast.literal_eval(index.readline())  # reads line then advances fp
                token = line[0]
                print(token)
                index_of_index[token] = current_fp    # map token to fp
            except SyntaxError:    # EOF
                print('Done.')
                print("Index for index in 'index_for_index.txt'")
                break
    return index_of_index

if __name__ == '__main__':
    i = create_index_for_index()
    with open('index_for_index.txt','w') as index_index:
        json.dump(i, index_index)
    

