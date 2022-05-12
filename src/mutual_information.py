# load libraries
import os
import re
import spacy
import math
import pandas as pd
import argparse 

def load_data(name):
    nlp = spacy.load("en_core_web_sm")
    filepath = os.path.join(
    "..", "CDS-LANG", "100_english_novels", "corpus", name)
    file_object = open(filepath, "r")
    text = file_object.read()
    text = text.lower() # make everything lower case
    text = re.sub("\W+", " ", text) # remove unwanted characters
    doc = nlp(text) # tokenize the text
    return doc

def collocate(term, doc):
    # count the amount of time the user-defined search_term appears in the text
    search_term = term
    counter = 0
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
    return search_term, counter, collocates

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
    for i in range(0, len(collocates)-1):
        another_counter = 0
        for token in collocates:
            if token.text == B_words:
                another_counter += 1
        AB.append(another_counter)
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
def save_results(collocates, B, AB, MI, csv_name):
    list_context = list(zip(collocates, B, AB, MI))
    dframe = pd.DataFrame(list_context, columns = ['words', 'B', 'AB', 'MI'])
    dframe = dframe.round(decimals = 2)
    dframe.to_csv(os.path.join("out", csv_name))
    return dframe
    
def parse_args():
    # initialize argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", required=True, help="the name of the file to load")
    ap.add_argument("-t", "--term", required=True, help="the user-defined search term")
    ap.add_argument("-c", "--csv_name", required=True, help="the name of the csv file to save")
    args = vars(ap.parse_args())
    return args

# let's run the code
def main():
    args = parse_args()
    doc = load_data(args["name"])
    search_term, counter, collocates = collocate(args["term"], doc)
    A, B, AB = freq(counter, collocates, doc)
    MI = mutual_information(doc, collocates, AB, A, B)
    dframe = save_results(collocates, B, AB, MI, args["csv_name"])

if __name__ == "__main__":
    main()
    

    
              
                           