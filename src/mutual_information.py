# load libraries
import os
import re
import spacy
import math
import pandas as pd
import argparse 

# let's load the data
def load_data(name):
    # initiate spacy model
    nlp = spacy.load("en_core_web_sm")
    filepath = os.path.join(
    "..", "CDS-LANG", "100_english_novels", "corpus", name)
    file_object = open(filepath, "r")
    text = file_object.read()
     # make everything lower case
    text = text.lower()
    # remove unwanted characters
    text = re.sub("\W+", " ", text)
    # tokenize the text
    doc = nlp(text)
    return doc

# create a function that finds that collocates of the user-defined search term
def collocate(term, doc):
    # count the amount of time the user-defined search_term appears in the text
    search_term = term
    # create counter
    counter = 0
    # for every token in the document
    for token in doc:
        # if the token is the search term
        if token.text == search_term:
            # add 1 to the counter 
            counter += 1
    # get the collocates
    # create an empty list
    collocates = []
    # for every token in the document
    for token in doc:
        # if the token is the search term
        if token.text == search_term:
            # get 5 tokens before
            before = token.i - 5
            # get 5 tokens after
            after = token.i + 5
            # for every token in that range
            for i in range(before, after):
                # if the text is not the search term (we don't want to include the search itself)
                if str(doc[i]) != search_term:
                    # append the text to the list
                    collocates.append(doc[i])
    return search_term, counter, collocates

# find the frequencies of the collocates
def freq(counter, collocates, doc):
    # define a counter
    A = counter
    # define an empty list
    B = []
    # for every collocate in the list in the range from 0 to the length of the collocate list
    for i in range(0, len(collocates)-1):
        # B_words are the collocates
        B_words = str(collocates[i])
        # define another counter
        new_counter = 0
        # for every token in the document
        for token in doc:
            # if the token is the search term
            if token.text == B_words:
                # append it to the counter
                new_counter += 1
        # append to the list      
        B.append(new_counter)
    # define a new list
    AB = []
    # for every collocate in the list in the range from 0 to the length of the collocate list
    for i in range(0, len(collocates)-1):
        # define another counter
        another_counter = 0
        # for every token in the collocate list
        for token in collocates:
            # if the token is the search term
            if token.text == B_words:
                # append it to the counter
                another_counter += 1
        # append to the list
        AB.append(another_counter)
    return A, B, AB

# calculate mutual information with the following formula:
# MI = log((AB*sizeCorpus)/(A*B*span))/log(2)
def mutual_information(doc, collocates, AB, A, B):
    # get the length of the document = corpus size
    text_length = len(doc)
    # define a span
    span = 10
    # define an empty list
    MI = []
    # for every token in the range between 0 and the length of the collocate list
    for i in range(0, len(collocates)-1):
        # get the mutual information score
        MI1 = math.log((AB[i] * text_length)/(A * B[i] * span))/math.log(2)
        # and append it to the list
        MI.append(MI1)
    return MI
        
# save results as csv 
def save_results(collocates, B, AB, MI, csv_name):
    # create list
    list_context = list(zip(collocates, B, AB, MI))
    # make that list into a dataframe
    dframe = pd.DataFrame(list_context, columns = ['words', 'B', 'AB', 'MI']).set_index("words")
    # round to 2 decimals
    dframe = dframe.round(decimals = 2)
    # save the csv with a user-defined name
    dframe.to_csv(os.path.join("out", csv_name))
    
    
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
    save_results(collocates, B, AB, MI, args["csv_name"])

if __name__ == "__main__":
    main()
    

    
              
                           
