import ast
import math
import json
"""

This function will normalize tf-df scores in the index 'final_index.txt'.

Writes to 'final_index_2.txt'

"""

def get_tf_idf_list(token):
    with open('final_index.txt','r') as index:
        fp = index_for_index[token]
        index.seek(fp)
        line = ast.literal_eval(index.readline())
        postings = line[1]
        return list(postings.values())

def calculate_denominator(tf_idf_list):
    sum = 0
    print(tf_idf_list)
    for score in tf_idf_list:
        sum += score ** 2
    return math.sqrt(sum)

def calculate_normalized(tf_idf, denominator):
    try:
        result = tf_idf / denominator
    except ZeroDivisionError:
        result = 1
    return result

def normalize():
    final_index_2 = open('final_index_2.txt','w')
    with open('final_index.txt','r') as index:
        while True:
            try:
                normalized_postings = {}
                line = ast.literal_eval(index.readline())
                postings = line[1]
                token = line[0]
                denominator = calculate_denominator(get_tf_idf_list(token))
                for doc, tf_idf in postings.items():
                    normalized_postings[doc] = calculate_normalized(tf_idf, denominator)
                new_tuple = (token, normalized_postings)
                final_index_2.write(str(new_tuple) + '\n')
                print(token)
            except SyntaxError:
                break


if __name__ == '__main__':
    with open('index_for_index.txt','r') as index_index:
        index_for_index = json.load(index_index)
    normalize()