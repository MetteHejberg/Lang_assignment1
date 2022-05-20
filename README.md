## 1. Assignment 1 - Collocation tool
Link to repository: https://github.com/MetteHejberg/Lang_assignment1

For this assignment, you will write a small Python program to perform collocational analysis using the string processing and NLP tools you've already encountered. Your script should do the following:

- Take a user-defined search term and a user-defined window size.
- Take one specific text which the user can define.
- Find all the context words which appear ± the window size from the search term in that text.
- Calculate the mutual information score for each context word.
- Save the results as a CSV file with (at least) the following columns: the collocate term; how often it appears as a collocate; how often it appears in the text; the mutual information score.

## 2. Methods
This assignment relates to the distributional hypothesis - that we can learn something about the meaning of a word from the other words around it. Therefore, this script how often a user-defined search term appears in a text, which other words appear with it, and calculates the frequency these words appear together with the search term with compared to when they don't to see how much these words add to the meaning of the search term.

The script allows the user to either load a single file or an entire directory. It firstly tokenizes the text(s) with ```spacy``` and thereafter gets the user-defined search term and finds its collocates. Then it finds the frequency of the collocates both on their own and as collocates. Lastly, it calculates the mutual information score on the basis of these things and saves a csv with the collocate words, frequency of the collocate in the text in general, frequency of the collocate as a collocate, and the mutual information score.

The mutual information score is calculated with the following formula: MI = log((AB*sizeCorpus)/(A*B*span))/log(2) 

Get the data here: 

## 3. Usage
To run the code you should:
- Pull this repository with this folder structure
- Place the texts in the ```in``` folder inside a folder called ```corpus```
- Install the packages mentioned in ```requirements.txt``` 
- Set your current working directory to the level above ```src```
- Write in the command line either: ```python src/mutual_information.py -f "file to use" -t "user-defined_search_term"``` or: ```python src/mutual_information.py -d "directory to use" -t "user-defined_search_term"```
  - The name of the text should be the name of one of the texts in the ```corpus``` folder
  - The csv in ```out``` was created with the following code in the terminal: ```python src/mutual_information.py -f "Bennet_Helen_1910.txt" - "park"```

## 4. Discussion of Results
While this approach gets quick results very easily, there are also more accurate and complex approaches such as word embeddings. Furthermore, the preprocessing of the text that makes everything lower case and removes unwanted characters could also potentially include removing stop words and/or converting all words to their lemmas. 

Eventhough this is a quick and easy approach, looking at the output and the words with the highest mutual information score, it does not seem, to me at least, that they reflect the meaning of "park" very much.
