import ast

merge_index = {}

def merge_indexes(counter, f1, f2):
    m = open('merges/merge' + str(counter) + '.txt', 'w')
    while True:
        try:
            k = ast.literal_eval(f1.readline())
            try:
                j = ast.literal_eval(f2.readline())
                k_token = k[0]
                j_token = j[0]
                k_posting = dict(k[1])
                j_posting = dict(j[1])

                ''' else if, k_tokens < j_tokens lexigraphically then iterate through till they're the same '''

                while k_token < j_token:
                    try:
                        merge_index[k_token] = k_posting
                        for item in merge_index.items(): 
                            m.write(str(item) + '\n')
                        merge_index.clear()
                        k = ast.literal_eval(f1.readline())
                        k_token = k[0]
                        k_posting = dict(k[1])
                    except:
                        try:
                            ''' f1 broke, so just do everything in f2 '''
                            while True:
                                j = ast.literal_eval(f2.readline())
                                j_token = j[0]
                                j_posting = dict(j[1])
                                for item in merge_index.items():
                                    m.write(str(item) + '\n')
                                merge_index.clear()
                        except:
                            break
                while k_token > j_token:
                    try:
                        merge_index[j_token] = j_posting
                        for item in merge_index.items():
                            m.write(str(item) + '\n')
                        merge_index.clear()
                        j = ast.literal_eval(f2.readline())
                        j_token = j[0]
                        j_posting = dict(j[1])
                    except:
                        try:
                            ''' f2 broke, write whatever is left in f1 '''
                            while True:
                                k = ast.literal_eval(f1.readline())
                                k_token = k[0]
                                k_posting = dict(k[1])
                                merge_index[k_token] = k_posting
                                for item in merge_index.items():
                                    m.write(str(item) + '\n')
                                merge_index.clear()
                        except:
                            break
                
                ''' if tokens are the same, then we want to append the postings '''

                if k_token == j_token:
                    k_posting.update(j_posting)
                    merge_index[k_token] = k_posting
                    for item in merge_index.items():
                        m.write(str(item) + '\n')
                    merge_index.clear()
                        
            except:
                try:
                    k = ast.literal_eval(f1.readline())
                    k_token = k[0]
                    k_posting = dict(k[1])
                    merge_index[k_token] = k_posting
                    for item in merge_index.items():
                        m.write(str(item) + '\n')
                    merge_index.clear()
                except:
                    break
        except:
            try:
                j = ast.literal_eval(f2.readline())
                j_token = j[0]
                j_posting = dict(j[1])
                for item in merge_index.items():
                    m.write(str(item) + '\n')
                merge_index.clear()
            except:
                break
    m.close()


# if __name__ == '__main__':
#     f11 = open('partials/partial_index1.txt', 'r')
#     f22 = open('partials/partial_index2.txt', 'r')
#     f33 = open('partials/partial_index3.txt', 'r')
#     merge_indexes(1,f11,f22)
#     m1 = open('merges/merge1.txt','r')
#     merge_indexes(2,m1,f33)
    



"""
f1 U f2 ... m1
m1 U f3 ... m2

m2 - final


m1 U f1 ... m1
m1 U f2 ... m2
m1 U f3 ... m3
"""


"""
.           .
.           .
.           air
air         airpod
airpod      .
.           .
.           .
.           .
.           .



"""