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

def get_cosine_similarity_list(query_scores: dict, postings: dict)->dict:
    ''' 
        query scores - {qt1: tf-idf1, qt2: tf-idf2, ... }
        postings - {pt1 : {docid : tf-idf1}, .... }
    ''' 
    if postings == None:
        return None
    result = {}
    # for term in query_scores.keys():
    #     numerator = 0
    #     q = 0
    #     d = 0
    #     for doc_id in postings[term].keys():
    #         numerator += query_scores[term] * postings[term][doc_id]
    #         q += query_scores[term] ** 2
    #         d += postings[term][doc_id] ** 2
    #         denominator = math.sqrt(q) * math.sqrt(d)
    #         cosine_sim = numerator/denominator
    #         all_postings[doc_id] = cosine_sim    
    for key, values in postings.items():
        for key1, value in values.items():
            cosine_doc = cosine_similiarity(query_scores,postings,key1)
            result[key1] = cosine_doc
    return result

def cosine_similiarity(query: dict, big_dict: dict, doc_number: int):
    q = 0
    d = 0
    numerator = 0
    for term in query.keys():
        numerator += query[term] * big_dict[term][doc_number]
        q += query[term] ** 2
        d += big_dict[term][doc_number] ** 2
    return numerator/(math.sqrt(q) * math.sqrt(d))

if __name__ == '__main__':




    print(calculate_query_scores(['master','of','master','engineering']))
