import ast


f1 = open('partials/partial_index1.txt', 'r')
f2 = open('partials/partial_index2.txt', 'r')
f3 = open('partials/partial_index3.txt', 'r')


merge_index = {}

def merge_indexes():
    try:    
        while True:
            k = ast.literal_eval(f1.readline())
            k_token = k[0]
            k_posting = k[1]
            merge_index[k_token] = k_posting            
    except:
        print("-- done -- ")

    try:
        while True:
            j = ast.literal_eval(f2.readline())
            j_token = j[0]
            j_posting = j[1]
            if j_token in merge_index:
                merge_index[j_token].update(j_posting)
            else:
                merge_index[j_token] = j_posting
    except:
        print("--- done --- ")



merge_indexes()
print(merge_index)

sorted_inverted_index = sorted(merge_index.items(), key= lambda kv: kv[0])
for item in sorted_inverted_index:
    print(item)