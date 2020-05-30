import ast
import math
import json
"""

This function will normalize tf-df scores in the index 'final_index.txt'.

Writes to 'final_index_2.txt'

"""

def get_tf_idf_list(token: str, index_for_index):
    with open('index/temp_index.txt','r') as index:
        fp = index_for_index[token]
        index.seek(fp)
        line = ast.literal_eval(index.readline())
        postings = line[1]
        return list(postings.values())

def calculate_denominator(tf_idf_list):
    sum = 0
    for score in tf_idf_list:
        sum += score ** 2
    return math.sqrt(sum)

def calculate_normalized(tf_idf, denominator):
    try:
        result = tf_idf / denominator
    except ZeroDivisionError:
        result = 1
    return result

def normalize(index_for_index):
    final_index = open('index/index.txt','w')
    with open('index/temp_index.txt','r') as index:
        curr_region = '0'
        print('Normalizing tf-idfs for tokens starting with: {}'.format(curr_region))
        while True:
            try:
                normalized_postings = {}
                line = ast.literal_eval(index.readline())
                postings = line[1]
                token = line[0]

                # Print current progress of what region of tokens are getting their posting lists changed
                if curr_region != str(token[0]):
                    curr_region = str(token[0])
                    print('Normalizing tf-idfs for tokens starting with: {}'.format(curr_region))

                denominator = _calculate_denominator(_get_tf_idf_list(token, index_for_index))
                for doc, tf_idf in postings.items():
                    normalized_postings[doc] = _calculate_normalized(tf_idf, denominator)
                new_tuple = (token, normalized_postings)
                final_index.write(str(new_tuple) + '\n')
            except SyntaxError:
                break


# if __name__ == '__main__':
#     with open('index/index_for_index.txt','r') as index_index:
#         index_for_index = json.load(index_index)
#     normalize()