# import libraries
import os
import re
import spacy
import math
import pandas as pd
import argparse

# load a single file
def load_data(name):
    filepath = os.path.join("in", "corpus", name)
    file_object = open(filepath, "r")
    text = file_object.read()
    # make everything lower case
    text = text.lower()
    # remove unwanted characters
    text = re.sub("\W+", " ", text)
    return text

# load an entire directory
def load_directory(directory): 
    path = os.path.join("in", directory)
    file_list = os.listdir(path)
    return path, file_list

# get the collocates
def collocate(term, text):
    # count the amount of time the user-defined search_term appears in the text
    # define search term
    search_term = term
    # define counter
    counter = 0
    # initialize spacy tokenizer 
    nlp = spacy.load("en_core_web_sm")
    # adjust max length of text
    nlp.max_length = 1500000
    # tokenize text
    doc = nlp(text)
    # for every token in the document
    for token in doc:
        # if the token.text is the search term
        if token.text == search_term:
            # count it
            counter += 1
    # get the collocates
    collocates = []
    # for every token in the document
    for token in doc:
        # if the token.text is the search term
        if token.text == search_term:
            # get five words before and after
            before = token.i - 5
            after = token.i + 5
            for i in range(before, after):
                if str(doc[i]) != search_term:
                    # append the collocates to the list
                    collocates.append(doc[i])
    return search_term, counter, doc, collocates

# find the frequencies of the collocates
def freq(counter, collocates, doc):
    A = counter
    # define list
    B = []
    # for every collocate in the list
    for i in range(0, len(collocates)-1):
        # B_words are the collocates
        B_words = str(collocates[i])
        new_counter = 0
        # for every token in the document
        for token in doc:
            # if the token.text is a collocate
            if token.text == B_words:
                # count it 
                new_counter += 1
        # append
        B.append(new_counter)
    # define empty list
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
     # corpus size
    text_length = len(doc)
    # define span
    span = 10
    # calculate MI
    MI = []
    for i in range(0, len(collocates)-1):
        MI1 = math.log((AB[i] * text_length)/(A * B[i] * span))/math.log(2)
        MI.append(MI1)
    return MI
        
# save results as csv 
def save_results(collocates, B, AB, MI, name):
    # create list out of lists
    list_context = list(zip(collocates, B, AB, MI))
    # convert to pandas dataframe
    dframe = pd.DataFrame(list_context, columns = ['Word', 'Frequency of word', 'Frequency as collocate', 'Mutual Information']).set_index("Word")
    # round to 2 decimals
    dframe = dframe.round(decimals = 2)
    # define outpath
    outpath = os.path.join("out", f"collocation_{name[0:name.index(f'.')]}.csv")
    # save as csv
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
    args = parse_args()
    if args["filename"] is not None and args["filename"].endswith(".txt"):
        print(f"[INFO]: Creating output")
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
    
