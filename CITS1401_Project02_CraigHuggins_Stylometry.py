# Project: Using Stylometry to Verify Authorship
# Author: Craig Ian Bond Huggins
# Version: 12
# Date: 24/10/2019
# Student ID: 22204675

import math
import os


# The generate_lists() function checks if the files provided exist. If they exist,
# the files are opened, read from, and the text is converted to lower-case for
# accurate comparison. Instances of double hyphen are converted to a space character.
# output: The list of words in each text file - for use by other functions.

def generate_lists(textfile1, textfile2):
    if not (os.path.isfile(textfile1)):
        return(None)
    if not (os.path.isfile(textfile2)):
        return(None)
    else:   #if the file does exist
        
        file1 = open(textfile1, 'r')
        file2 = open(textfile2, 'r')
        file1_text = file1.read()
        file2_text = file2.read()
        file1_text = file1_text.lower()
        file2_text = file2_text.lower()
        
        for word in file1_text:
            file1_text = file1_text.replace('--', " ")
        for word in file2_text:
            file2_text = file2_text.replace('--', " ")
            
        list_file1 = file1_text.split()
        list_file2 = file2_text.split()
        
        file1.close()
        file2.close()
                    
    return list_file1, list_file2



# In the conjunctions() function, dictionaries are created for all conjunction-type
# words, which have an initial value of 0. For all instances of conjunction words
# found in each text, the count for that word is increased by 1 in the corresponding
# dictionary. Un-needed punctuation is removed for enhanced accuracy.
# output: completed 'conjunctions' profiles 1 and 2

def conjunctions(textfile1, textfile2):
    document1, document2 = generate_lists(textfile1, textfile2)

    count_conjunctions_1 = dict()
    count_conjunctions_2 = dict()
    
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''   # string of all punctuation to be removed
    
    conjunction_list = ["also", "although", "and", "as", "because",
                        "before", "but", "for", "if", "nor", "of", "or",
                        "since", "that", "though", "until", "when", "whenever",
                        "whereas", "which", "while", "yet"]
    
    for word in conjunction_list:
        count_conjunctions_1[word] = count_conjunctions_1.get(word,0)
        count_conjunctions_2[word] = count_conjunctions_2.get(word,0)
    
    for word in document1:
        word = word.strip(punctuations)
        if word in count_conjunctions_1:
            count_conjunctions_1[word] += 1 
    for word in document2:
        word = word.strip(punctuations)
        if word in count_conjunctions_2:
            count_conjunctions_2[word] += 1
    
    return count_conjunctions_1, count_conjunctions_2



def unigrams(textfile1, textfile2):
    document1, document2 = generate_lists(textfile1, textfile2)
    count_unigrams_1 = dict()
    count_unigrams_2 = dict()
    
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''   # string of all punctuation to be removed
    
    for word in document1:
        word = word.strip(punctuations)
        if word in count_unigrams_1:
            count_unigrams_1[word] += 1
        else:
            count_unigrams_1[word] = 1
            
    for word in document2:
        word = word.strip(punctuations)
        if word in count_unigrams_2:
            count_unigrams_2[word] += 1
        else:
            count_unigrams_2[word] = 1
    
    return count_unigrams_1, count_unigrams_2



# The punctuation() function opens the provided text file's, splits the text into
# individual letters, and then adds the letters to a new list. The list of letters
# for each document is then iterated over, checking for instances of punctuation
# characters single-quote and hyphen, and whether they are surrounded by alphabetic
# letters, in which case their count is then increased. The count of comma and semicolon
# is increased regardless of their position in-text. An IndexError exception has been
# added for checking the letter's before and after the current index character, in cases
# where the found punctuation character is the very first or very last character in a
# line and the index goes out of bounds.
# output: completed 'punctuation' profiles 1 and 2

def punctuation(textfile1, textfile2):
    
    if not (os.path.isfile(textfile1)):
        return(None)
    if not (os.path.isfile(textfile2)):
        return(None)
    
    with open(textfile1) as file1:
        list_letters1 = [list(line.rstrip()) for line in file1]
    with open(textfile2) as file2:
        list_letters2 = [list(line.rstrip()) for line in file2]
        
    list1 = []
    list2 = []
    
    for i in range(len(list_letters1)):
        for e in range(len(list_letters1[i])):
            list1.append(list_letters1[i][e])
            
    for i in range(len(list_letters2)):
        for e in range(len(list_letters2[i])):
            list2.append(list_letters2[i][e])

    count_punctuation_1 = dict()
    count_punctuation_2 = dict()
    
    punctuation_insideword_list = ["'", '-']
    punctuation_outsideword_list = [',', ';']
    
    for symbol in punctuation_insideword_list:
        count_punctuation_1[symbol] = count_punctuation_1.get(symbol,0)
        count_punctuation_2[symbol] = count_punctuation_2.get(symbol,0)
    for symbol in punctuation_outsideword_list:
        count_punctuation_1[symbol] = count_punctuation_1.get(symbol,0)
        count_punctuation_2[symbol] = count_punctuation_2.get(symbol,0)
    
    try:
        for i in range(len(list1)):
            if list1[i] in punctuation_insideword_list:
                if list1[i-1].isalpha() and list1[i+1].isalpha():
                    count_punctuation_1[list1[i]] += 1
            elif list1[i] in punctuation_outsideword_list:
                count_punctuation_1[list1[i]] += 1
    except IndexError:
        pass
    
    try:
        for i in range(len(list2)):
            if list2[i] in punctuation_insideword_list:
                if list2[i-1].isalpha() and list2[i+1].isalpha():
                    count_punctuation_2[list2[i]] += 1
            elif list2[i] in punctuation_outsideword_list:
                count_punctuation_2[list2[i]] += 1
    except IndexError:
        pass
    
    return count_punctuation_1, count_punctuation_2
      
      
      
# The composite() function receives the completed Dictionaries from the conjunctions()
# and punctuation() functions. These dictionaries are then merged into a new composite
# dictionary for each document. The provided text files are opened and read from, and
# then separated into Paragraphs and Sentences. A paragraph is considered to be where
# two new-line characters are encountered. A sentence is considered where various character
# criteria is found, such as a full-stop followed by a quotation mark. Where encountered,
# this criteria is replaced with a standard full-stop followed by a space, simply for
# convenience purposes in order to split the text successfully.
# output: completed 'composite' profiles 1 and 2

def composite(textfile1, textfile2):
    
    if not (os.path.isfile(textfile1)):
        return(None)
    if not (os.path.isfile(textfile2)):
        return(None)
    
    dict_conjunction1, dict_conjunction2 = conjunctions(textfile1, textfile2)
    dict_punctuation1, dict_punctuation2 = punctuation(textfile1, textfile2)
    
    count_composite_1 = dict_conjunction1   # new composite Dictionary is a copy of the original conjunction Dictionary
    count_composite_2 = dict_conjunction2
    
    count_composite_1.update(dict_punctuation1)   # update composite Dictionary to include punctuation
    count_composite_2.update(dict_punctuation2)
    
    file1 = open(textfile1, 'r')
    file2 = open(textfile2, 'r')
    file1_text = file1.read()
    file2_text = file2.read()
    file1_text = file1_text.lower()
    file2_text = file2_text.lower()
        
    for word in file1_text:
        file1_text = file1_text.replace('--', " ")
    for word in file2_text:
        file2_text = file2_text.replace('--', " ")
                
    file1_text_paragraphs = file1_text.split('\n\n')   #\n\n indicates a new paragraph 
    file2_text_paragraphs = file2_text.split('\n\n')
    
    for word in file1_text:
        file1_text_new = file1_text.replace('.\n', '. ').replace('."', '. ').replace('?"', '. ').replace('!"', '. ').replace('? ', '. ').replace('! ', '. ')   #replace the new paragraph indicator with ". "
    for word in file2_text:
        file2_text_new = file2_text.replace('.\n', '. ').replace('."', '. ').replace('?"', '. ').replace('!"', '. ').replace('? ', '. ').replace('! ', '. ')    #replace the new paragraph indicator with ". "
        
    file1_text_sentences = file1_text_new.split('. ')
    file2_text_sentences = file2_text_new.split('. ')
    
    for sentence in file1_text_sentences:
        if sentence == '':
            file1_text_sentences.remove(sentence)   #remove any empty sentences
            
    for sentence in file2_text_sentences:
        if sentence == '':
            file2_text_sentences.remove(sentence)
    
    new_list1 = []
    new_list2 = []
    
    number_sentences_text1 = len(file1_text_sentences)
    number_sentences_text2 = len(file2_text_sentences)
        
    for i in range(len(file1_text_paragraphs)):
        if file1_text_paragraphs[i] != '':
            new_list1.append(file1_text_paragraphs[i])
        
    for i in range(len(file2_text_paragraphs)):
        if file2_text_paragraphs[i] != '':
            new_list2.append(file2_text_paragraphs[i])
            
    number_paragraphs_doc1 = len(new_list1)
    number_paragraphs_doc2 = len(new_list2)
    
    average_sentences_per_paragraph_text1 = number_sentences_text1 / number_paragraphs_doc1
    average_sentences_per_paragraph_text2 = number_sentences_text2 / number_paragraphs_doc2
    
    unigrams_doc1, unigrams_doc2 = unigrams(textfile1, textfile2)   #receive the total count of each word in the files from the unigrams() function
    
    sum_words_doc1 = sum(unigrams_doc1.values())
    sum_words_doc2 = sum(unigrams_doc2.values())
    
    average_words_per_sentence1 = sum_words_doc1 / number_sentences_text1
    average_words_per_sentence2 = sum_words_doc2 / number_sentences_text2
    
    composite_dict_1 = {"words_per_sentence" : round(average_words_per_sentence1, 4) , "sentences_per_paragraph" : average_sentences_per_paragraph_text1}
    composite_dict_2 = {"words_per_sentence" : round(average_words_per_sentence2, 4) , "sentences_per_paragraph" : average_sentences_per_paragraph_text2}
    
    count_composite_1.update(composite_dict_1)
    count_composite_2.update(composite_dict_2)
    
    file1.close()
    file2.close()
    
    return count_composite_1, count_composite_2
    
    
    
# The main() function checks that the two provided text files exist. If they do,
# the feature provided by the user must match one of the available functions in
# the program. The appropriate function is called, and the two profiles receive
# data from the functions. The distance is calculated based on the differences
# in values between Profile 1 and Profile 2.
# outputs: The calculated Distance, Profile 1 and Profile 2

def main(textfile1, textfile2, feature):
    if not (os.path.isfile(textfile1)):
        return None, None, None
    if not (os.path.isfile(textfile2)):
        return None, None, None
    
    if feature == 'conjunctions':
        profile1, profile2 = conjunctions(textfile1, textfile2)
    elif feature == 'unigrams':
        profile1, profile2 = unigrams(textfile1, textfile2)
    elif feature == 'punctuation':
        profile1, profile2 = punctuation(textfile1, textfile2)
    elif feature == 'composite':
        profile1, profile2 = composite(textfile1, textfile2)
    else:
        return None, None, None
    
    dict_differences = {x: profile1[x] - profile2[x] for x in profile1 if x in profile2}   #the difference between values if the key exists in both profiles
    for k, v in dict_differences.items():
        dict_differences[k] = abs(v)
        dict_differences[k] = math.pow(dict_differences[k], 2)

    difference_value = sum(dict_differences.values())
    distance = round(math.sqrt(difference_value),4)
    
    return distance, profile1, profile2
