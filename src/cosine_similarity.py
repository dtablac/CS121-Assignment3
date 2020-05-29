from normalize import *
from ranking import *
from PartA import computeWordFrequencies

"""

This program will compute cosine similarity for each token between query and doc

"""

def calculate_query_scores(query_terms: list):
    ''' Compute tf, then tf-idf, then normalize for each query term '''
    query_scores = computeWordFrequencies(query_terms) # dict
    count = len(query_scores)

    for token, tf in query_scores.items():
        query_scores[token] = calculate_tf_idf(tf, count, tf)

    denominator = calculate_denominator(list(query_scores.values()))

    for token, tf_idf in query_scores.items():
        query_scores[token] = calculate_normalized(tf_idf, denominator)

    return query_scores

def cosine_similarity(query_scores: dict, postings: dict)->dict:
    all_postings = []
    for term in query_scores.keys():
        


    return result

            

if __name__ == '__main__':




    print(calculate_query_scores(['master','of','master','engineering']))
