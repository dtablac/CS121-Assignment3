import sys, os.path, string, re
from os import path

# Please note that this program will only run on python 3.x.x (So, use python3 and not python if it is not)

"""
    Takes a file path and opens the file if exists.
    then reads the file and reads the contents onto a string which
    will then be later used to "tokenized" into a list.
    input: string
    output: list; unless error occurs -1.

    runtime complexity: 
        n = characters, m = token size
        reading from a file and storing its content = O(n)
        converting all punctuation to spaces = O(n)
        looping through our content = O(n)
            checking if token are greater than or equal to size 2 = O(1)
            checking if token is alphanumeric and checking if it contains english letters = O(m)
                appending token and making lower case = O(1) * O(m) = O(m)
                ~ O(m^2)
            ~O(n*m^2)

        therefore; our algorithm runs at a complexity of O(n * m^2)
        however, assume that m is very miniscule (not that big of a word)
        we can say that our algorithm complexity is O(n) because O(m^2) can be treated as constant
        since O(m^2) would be very tiny or in most cases n > m^2 and we'd have something such that
        O(Cn). So in reality O(n) unless otherwise (correct me if im wrong).
        
        tldr: O(n)

"""
def tokenize(file_path) -> list:
    if not file_check(file_path):
        return -1                                       # return -1 if path doesnt exists
    else:
        more_restrictful_alphanum = re.compile(r'^[0-9A-Za-z]*$')               # alphanum() allows non-english characters
        file = open(file_path,"r")                                              # open our file
        tokens = []
        content = file.read()                                                   # put the contents in our file in a string
        content = content.translate(str.maketrans(string.punctuation,' ' * len(string.punctuation)))   # treat all punctuation's as spaces.
        content = content.split()                                               # convert our string into a list of tokens.
        for token in content:                                                   # iterate through our raw tokens
            if len(token) >= 2 and more_restrictful_alphanum.match(token):      # only add the "token" to our tokens list if
                tokens.append(token.lower())                                    # it satisfies our constraint
        file.close()
        return tokens                                                           
""" 
    count how many times a word occurs within our list of tokens. 
    input: list
    output: dict

    runtime complexity:
        iterating through tokens = O(n)
            checking if token is in table = O(1)
                adding/updating values in table = O(1)
        Therefore, our algorithm complexity is O(n)

        tldr: O(n)
"""
def computeWordFrequencies(tokens) -> dict:
    frequency_table = {}                                                        # create our dictionary
    for token in tokens:                                                        # for every token in tokens
        if token in frequency_table:                                            # if our token is in the table already
            frequency_table[token] = frequency_table[token] + 1                 # add one to the current value
        else:
            frequency_table[token] = 1                                          # else just start a new one
    return frequency_table                                                      # return the table

"""
    print the entire dictionary with well format.
    
    runtime complexity:
        iterate through our dictionary of tokens and their frequencies = O(n)
        Therfore, our algorithm complexity is O(n)

        tldr: O(n)
"""
def printWordFrequencies(token_frequencies):
    for key, value in token_frequencies.items():
        print(key + " -> " + str(value))

""" 
    check if the file path is valid
"""
def file_check(file_path):
    return path.exists(file_path) and path.isfile(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expected 1 arguement instead got " + str(len(sys.argv) - 1))
    else:
        file_name = sys.argv[1]
        tokenize_list = tokenize(file_name)
        if tokenize_list == -1:
            print("file path does not exists or is not a file.")
        else:
            if tokenize_list == []:
                print("Your text file was empty")
            else:
                frequency_table = computeWordFrequencies(tokenize_list)
                printWordFrequencies(frequency_table)
