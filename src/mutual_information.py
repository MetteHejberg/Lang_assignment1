import os
import re
import spacy
import math
import pandas as pd
import argparse

def load_data(name):
    filepath = os.path.join("..", "CDS-LANG", "100_english_novels", "corpus", name)
    file_object = open(filepath, "r")
    text = file_object.read()
    return text

def load_directory(directory): # I got this function from Agnes
    path = os.path.join("..", "CDS-LANG", "100_english_novels", directory)
    file_list = os.listdir(path)
    return path, file_list

def collocate(term, text):
    # count the amount of time the user-defined search_term appears in the text
    search_term = term
    counter = 0
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1500000
    doc = nlp(text)
    for token in doc:
        if token.text == search_term:
            counter += 1
    # get the collocates
    collocates = []
    for token in doc:
        if token.text == search_term:
            before = token.i - 5
            after = token.i + 5
            for i in range(before, after):
                if str(doc[i]) != search_term:
                    collocates.append(doc[i])
    return search_term, counter, doc, collocates

# find the frequencies of the collocates
def freq(counter, collocates, doc):
    A = counter
    B = []
    # for every collocate in the list
    for i in range(0, len(collocates)-1):
        # B_words are the collocates
        B_words = str(collocates[i])
        new_counter = 0
        for token in doc:
            if token.text == B_words:
                new_counter += 1
        B.append(new_counter)
    
    AB = []
    # for every collocate in the text 
    for i in range(0, len(collocates)-1): 
        # define B_words which is the collocates 
        B_words = str(collocates[i])
        # and define a counter 
        counter4 = 0 
        # for every token in the list 
        for token in collocates:
            # if the token is a collocate 
            if token.text == B_words:
                # count it 
                counter4 += 1
                 # and append to the empty list         
        AB.append(counter4)
    return A, B, AB

# calculate mutual information with the following formula:
# MI = log((AB*sizeCorpus)/(A*B*span))/log(2)
def mutual_information(doc, collocates, AB, A, B):
    text_length = len(doc) # corpus size
    span = 10
    MI = []
    for i in range(0, len(collocates)-1):
        MI1 = math.log((AB[i] * text_length)/(A * B[i] * span))/math.log(2)
        MI.append(MI1)
    return MI
        
# save results as csv 
def save_results(collocates, B, AB, MI, name):
    list_context = list(zip(collocates, B, AB, MI))
    dframe = pd.DataFrame(list_context, columns = ['Word', 'Frequency of word', 'Frequency as collocate', 'Mutual Information']).set_index("Word")
    dframe = dframe.round(decimals = 2)
    outpath = os.path.join("out", f"collocation_{name[0:name.index(f'.')]}.csv")
    dframe.to_csv(outpath)
    
def parse_args():
    # initialize argparse
    ap = argparse.ArgumentParser()
    # add command line parameters 
    ap.add_argument("-f", "--filename", required=False, help="The filename to use")
    ap.add_argument("-d", "--directory", required=False, help="The directory to use")
    ap.add_argument("-t", "--term", required=True, help="the user-defined search term")
    args = vars(ap.parse_args())
    # return list og arguments
    return args   

# let's run the code
def main():
    #args = parse_args()
    #doc = load_data(args["name"])
    #search_term, counter, collocates = collocate(args["term"], doc)
    #A, B, AB = freq(counter, collocates, doc)
    #MI = mutual_information(doc, collocates, AB, A, B)
    #dframe = save_results(collocates, B, AB, MI, args["csv_name"])

    args = parse_args()
    if args["filename"] is not None and args["filename"].endswith(".txt"):
        text = load_data(args["filename"])
        search_term, counter, doc, collocates = collocate(args["term"], text)
        A, B, AB = freq(counter, collocates, doc)
        MI = mutual_information(doc, collocates, AB, A, B)
        save_results(collocates, B, AB, MI, args["filename"])
    elif args["directory"] is not None:
        results = load_directory(args["directory"])
        for filename in results[1]:
            if filename.endswith(".txt"):
                path = f"{results[0]}/{filename}"
                print(f"[INFO]: Creating {filename} output")
                text = load_data(filename)
                search_term, counter, doc, collocates = collocate(args["term"], text)
                A, B, AB = freq(counter, collocates, doc)
                MI = mutual_information(doc, collocates, AB, A, B)
                save_results(collocates, B, AB, MI, filename)
            else:
                pass
    else:
        pass    
    
if __name__ == "__main__":
    main()
    
