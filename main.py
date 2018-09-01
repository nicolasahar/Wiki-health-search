# *** CODE FOR PAGES 1-3 ***

import os
import math

# Redefine this constant to be the path to where you stored the unzipped
# wikipages. The Windows OS uses \ as the directory separator and inside
# this constant string you need two slashes for each separator.
# For example "C:\\user\\folder\\subfolder\\"
HOMEFOLDER = "/Users/nicolasahar/Desktop/ECs/2015-2016/Computing for Medicine (Apr 2016)/Assignments/Assignment 1 (due June 24)/Files/wikipages/"
#HOMEFOLDER = "/Users/mcraig/admin/Activity2016/cs_for_docs/workshops/diagnosis_tfidf/wikipages/"
PUNCTUATION = """.,<>;'":{}[]|!@#$%^&*()"""

def clean_up(text):
    """ (string) -> (string)

    Return a version of the string text where all the letters have been
    converted to lower case, and all punctuation was replaced with whitespaces

    >>> clean_up('Influenza, commonly known as "the flu", is ...')
    'influenza  commonly known as  the flu   is    '
    """

    cleaned_str = []

    for char in text:
        if char in PUNCTUATION:
            cleaned_str.append(" ")
        else:
            cleaned_str.append(char.lower())

    return "".join(cleaned_str)

## Test case for def clean_up(text): returns true
# print(clean_up("Influenza, commonly known as \"the flu\", is ...") == ("influenza  commonly known as  the flu   is    "))

def get_all_texts(datapath):
    """ (string) -> dict of {string: string}

    Return a dictionary where the keys are disease names
    and the values are the contents of the file key.html
    from the directory datapath.
    """

    # get a list of all the filenames in the directory
    filenames = os.listdir(datapath)

    # dictionary of all texts, keys are disease names
    disease_to_text= {}

    for filename in filenames:

        # only consider filenames that end in ".html"
        if len(filename) > 5  and  filename[-5:] == ".html":

            # read the entire file's contents as a string
            text = open(datapath + filename).read()
            # since all the filenames end in .html, just drop that part
            disease = filename[:-5]
            # insert it into the dictionary
            disease_to_text[disease] = clean_up(text)

    return disease_to_text

##Reading in and pre-processing the documents
# print(get_all_texts(HOMEFOLDER))

def keyword_found(keyword, doc_name, disease_to_text):
    """ (str, str, dict of {str:str}) -> bool

    Return True iff keyword is found in this doc_name inside disease_to_text
    as a full token separated by whitespace.

    """
    if keyword in disease_to_text[doc_name].split(): #Note: don't need to worry about punctuation in the tokens as it has all been removed!
        return True
    else:
        return False

## Test cases for keyword_found
# print(keyword_found("hello", "dict1", {"dict1": "hello my name is nick"}) == True)
# print(keyword_found("deafness", "Mumps", get_all_texts(HOMEFOLDER))) # correctly returns True
# print(keyword_found("deafness", "Typhus", get_all_texts(HOMEFOLDER))) # correctly returns False
# print(keyword_found("bacteria", "Typhus", get_all_texts(HOMEFOLDER))) # correctly returns True
# print(keyword_found("bacteria", "Mumps", get_all_texts(HOMEFOLDER))) # correctly returns False

def idf(keyword, disease_to_text):
    """ (str, dict of {str: str}) -> float

    """
    count = 0

    for doc_name in disease_to_text:
        if keyword_found(keyword, doc_name, disease_to_text):
            count += 1
    try:
        return math.log(len(disease_to_text)/count) #Note: math.log uses base e by default, not base 10. I left it as base e as the base used is "not material to the ranking", according to this source: http://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html

    except ZeroDivisionError: #occurs when count = 0 (i.e. keyword is not found in any of the documents)
        return -1

## Test cases for idf:
# print(idf("hello", {1:"hello", 2: "hello my", 3: "hello my name", 4: "hi", 5: "no"})) # correctly returns 0.51 (i.e. ln(5/3))
# print(idf("deafness", get_all_texts(HOMEFOLDER))) #correctly returns 4.15 (i.e. ln(382/6))
# print(idf("fever", get_all_texts(HOMEFOLDER))) #correctly returns 0.49 (i.e. ln(382/234))
# print(idf("bacteria", get_all_texts(HOMEFOLDER))) #correctly returns 0.49 (i.e. ln(382/233))
# print(idf("the", get_all_texts(HOMEFOLDER))) #correctly returns 0.0 (i.e. ln(382/382))
# print(idf("parotid", get_all_texts(HOMEFOLDER))) #correctly returns 4.33 (i.e. ln(382/5)); note that "parotid" actually appears in 5 documents, not 4 as indicated in the instructions handout (To check, I printed all doc_names that returned True for containing "parotid" and I opened the html file and searched for "parotid". The word was present in all 5 cases.
# print(idf("notfound", get_all_texts(HOMEFOLDER))) #correctly returns 4.15 (i.e. ln(382/6))

def tf_idf(keyword, doc_name, disease_to_text, score):

    count = 0

    for word in disease_to_text[doc_name].split():
        if word == keyword:
            count += 1

    len_doc = len(disease_to_text[doc_name].split())

    return (count/len_doc) * score #part 2 of bells and whistles - normalizing for length of wiki page, so divide count by len(doc_name)

## Test Cases for tf_idf: testing count only
# print(tf_idf("bacteria", "Typhus", get_all_texts(HOMEFOLDER))) #correctly returns count of 5
# print(tf_idf("parotid", "Melioidosis", get_all_texts(HOMEFOLDER))) #correctly returns count of 3
# print(tf_idf("parotid", "Mumps", get_all_texts(HOMEFOLDER))) #correctly returns count of 11

## Test Cases for tf_idf: testing tf_idf scores only (from Bells and Whistles, part 1), but before normalization (from Bells and Whistles, part 2)
# print(tf_idf("bacteria", "Typhus", get_all_texts(HOMEFOLDER), idf("bacteria", get_all_texts(HOMEFOLDER)))) #correctly returns score of 2.47 (TF = 5; IDF = 0.49)
# print(tf_idf("parotid", "Melioidosis", get_all_texts(HOMEFOLDER), idf("parotid", get_all_texts(HOMEFOLDER)))) #correctly returns score of 13 (TF = 3; IDF = 4.33)
# print(tf_idf("parotid", "Mumps", get_all_texts(HOMEFOLDER), idf("parotid", get_all_texts(HOMEFOLDER)))) #correctly returns score of 47.7 (TF = 11; IDF = 4.33)

## Test Cases for tf_idf: testing tf_idf scores only (from Bells and Whistles, part 1), and with normalization (from Bells and Whistles, part 2)
# print(tf_idf("bacteria", "Typhus", get_all_texts(HOMEFOLDER), idf("bacteria", get_all_texts(HOMEFOLDER)))) #returns score of 0.00017 (lendoc_name = 14645, TF = 0.0003; IDF = 0.49)


def build_empty_scores_dict(disease_to_text):
    """ (dict of {str:str}) -> dict of {str:number}
    Build and return an empty dictionary where the keys are the same as the keys in disease_to_text
    and the values are all 0.
    """

    current_scores = {}

    for doc_name in disease_to_text:
        current_scores[doc_name] = 0

    return current_scores

## Test for build_empty_scores_dict:
# print(build_empty_scores_dict(get_all_texts(HOMEFOLDER)))

def update_scores(current_scores, keyword, all_texts):
    """ (dict of {str: number}, str, dict of {str: str}) -> None

    Update current_scores by adding to the value of each entry to TF-IDF individual score
    for keyword based on the documents in all_texts.

    """

    score = idf(keyword, all_texts) # satisfies "Being Efficient"

    if score == -1:
        pass #score is actually 0, as the keyword does not appear in any document

    else:
        for doc_name in all_texts:
            if keyword_found(keyword, doc_name, all_texts):
                current_scores[doc_name] += tf_idf(keyword, doc_name, all_texts, score)

    return current_scores

# Note: current_scores = build_empty_scores_dict(disease_to_text), disease_to_text = get_all_texts(HOMEFOLDER)

## Test cases for update_scores (without tf_idf)
# print(update_scores(build_empty_scores_dict(get_all_texts(HOMEFOLDER)), "bacteria", get_all_texts(HOMEFOLDER))) #correctly updates bacteria's IDF for Typhus (0.49) and Mumps (0.0), as bacteria is found in Typhus but not in Mumps
# print(update_scores(build_empty_scores_dict(get_all_texts(HOMEFOLDER)), "deafness", get_all_texts(HOMEFOLDER))) #correctly updates deafness' IDF for Typhus (0.0) and Mumps (4.15), as deafness is found in Mumps but not in Typhus

## Test cases for update_scores, with tf_idf (from Bells and Whistles, part 1) but before normalization (from Bells and Whistles, part 2)
# print(update_scores(build_empty_scores_dict(get_all_texts(HOMEFOLDER)), "bacteria", get_all_texts(HOMEFOLDER))) #correctly updates bacteria's TF-IDF for Typhus (2.47) and Mumps (0.0), as bacteria is found in Typhus but not in Mumps

## Test cases for update_scores, with tf_idf (from Bells and Whistles, part 1) and after normalization (from Bells and Whistles, part 2)
# print(update_scores(build_empty_scores_dict(get_all_texts(HOMEFOLDER)), "bacteria", get_all_texts(HOMEFOLDER))) #correctly updates bacteria's TF-IDF for Typhus (0.00017) and Mumps (0.0), as bacteria is found in Typhus but not in Mumps

# ***CODE FOR PAGE 3 - PUTTING IT ALL TOGETHER - only returns the MOST relevant document(s)***

def most_relevant_documents(dict):

    score_dict = build_empty_scores_dict(dict)
    keywords = ""

    while keywords != "quit":

        keywords = input("Enter your keywords, please: ")

        if keywords == "quit":
            break

        #cleaning
        keyword_list = []

        for char in keywords:
            if char in PUNCTUATION:
                keyword_list.append("")
            else:
                keyword_list.append(char.lower())

        keyword_list =("".join(keyword_list)).split(" ")

        #update scores
        for keyword in keyword_list:
            update_scores(score_dict, keyword, dict)

        #return highest scoring
        max_score_list = []
        max_score = 0

        for doc_name in score_dict:
            if score_dict[doc_name] > max_score:
                del(max_score_list[:])
                max_score_list.append(doc_name)
                max_score = score_dict[doc_name]

            elif score_dict[doc_name] == max_score:
                max_score_list.append(doc_name)

        #To account for the possibility of no matches (all scores = 0) or for multiple top matches (with equal scores)
        if max_score == 0:
            alert = "Alert: There were no relevant matches for your keywords. Please try again.\n"
            max_score_list = "None"
        elif len(max_score_list) > 1:
            alert = "Alert. There were %s matches with equal top scores.\n" %(len(max_score_list))
        else:
            alert =""

        print("Top match(es): %s \nScore: %s \n%s" %(max_score_list, max_score, alert))

        for doc_name in score_dict:
            score_dict[doc_name] = 0

## Test Dictionary
# print(most_relevant_documents({"a": "a b c d e", "b": "a b e h", "c": "i j k"}))

## Actual Dictionary ** print this for FINAL implementation of entire program - without multiple matches returned **
# print(most_relevant_documents(get_all_texts(HOMEFOLDER)))

## Test Cases (using Test Dictionary):
# Input: "a"; # correctly returns top match for input "a" (document "b") and correct top score (0.101)
# Input: "5"; # correctly returns no top matches for input "5") (no scores > 0)
# Input: "c"; # correctly returns top match for input "c" (document "a") and correct top score (0.219)

## Test Cases (using Actual Dictionary): before TF-IDF implementation (from Bells and Whistles)
# Testing "updating_scores": Input: "bacteria", fever; correctly returns 0.98 for "Spirochaete" (both terms found) and 0.00 for "Gerstmann-Str%C3%A4ussler-Scheinker_syndrome" (no terms found)
# Testing "most_relevant_documents": Input: "parotid"; correctly returns 4.33 for "Spirochaete" and the 5 most relevant documents with this score

## Test Cases (using Actual Dictionary): after TF-IDF implementation (from Bells and Whistles, part 1), but before normalization (from Bells and Whistles, part 2)
# Testing "most_relevant_documents": Input: "bacteria"; correctly returns 2.47 for "Typhus" and the most relevant article ("Bacteria") with a score of 169

## Test Cases (using Actual Dictionary): after TF-IDF implementation (from Bells and Whistles, part 1), and after normalization (from Bells and Whistles, part 2)
# Testing "most_relevant_documents": Input: "bacteria"; correctly returns most relevant article ("Clostridium_difficile_(bacteria)") for input "bacteria" with a score of 0.0025
# Testing "most_relevant_documents": Input: "parotid"; correctly returns most relevant article ("Mumps") for input "parotid" with a score of 0.0021


# ***CODE FOR PAGE 4 - BELLS AND WHISTLES***

# Part 1 - adjusting the formula for keywork frequency in a document: done above in a NEW function called (tf_idf)
# Part 2 - adjusting the algorithm to account for how common the disease is via using the length of the wikipedia page as proxy: done above in a NEW function called (tf_idf)

# Part 3 - have the query return the top N matches rather than just the top match

def top_n_matches(dict):

    score_dict = build_empty_scores_dict(dict)
    keywords = ""

    while keywords != "quit":

        keywords = input("Enter your keywords, please: ")

        if keywords == "quit":
            break

        num_matches = int(input("How many matches do you want to view? "))

        #cleaning
        keyword_list = []

        for char in keywords:
            if char in PUNCTUATION:
                keyword_list.append("")
            else:
                keyword_list.append(char.lower())

        keyword_list =("".join(keyword_list)).split(" ")

        #update scores
        for keyword in keyword_list:
            update_scores(score_dict, keyword, dict)

        #return highest scoring
        doc_list = []
        score_list = [] # keeps track of the number of matches (relevant match = document with score > 1

        for doc_name in score_dict:
            for i in range(len(score_dict)): #for every doc_name's score, check if its score is greater than each score in the score_list, starting from index 0; if it's greater than the score at index x, insert that score and its doc_name into both doc_list and score_list at index x; if not greater, check the next index (x+1) until you find: a. an index with a lower score; or b. reach the end of the list, at which point, append the score/docname to the end of the two lists

                if score_dict[doc_name] == 0: #don't want to risk returning matches with 0 score if there are not enough matches with score > 0
                    break

                elif score_list == [] and doc_list == []:
                    doc_list.append(doc_name)
                    score_list.append(score_dict[doc_name])
                    break

                elif score_dict[doc_name] > score_list[i]:
                    doc_list.insert(i, doc_name)
                    score_list.insert(i, score_dict[doc_name])
                    break

                elif i == len(score_list)-1:
                    doc_list.append(doc_name)
                    score_list.append(score_dict[doc_name])
                    break

        # Accounting for the possibility of less relevant matches (relevant match = docname with score > 0) than # of top matches requested
        if len(score_list) == 0:
            alert = "Alert: There were no relevant matches for your keywords. Please try again.\n"
        elif len(score_list) < num_matches and len(score_list) == 1:
            alert = "Alert: You requested the top %s matches, but there was only 1 relevant match.\n" %(num_matches)
        elif len(score_list) < num_matches and len(score_list) > 1:
            alert = "Alert: You requested the top %s matches, but there were only %s relevant matches.\n" %(num_matches, len(score_list))
        else:
            alert = ""

        print("Top match(es): %s \nScores for top match(es): %s \n%s" %(doc_list[:num_matches], score_list[:num_matches], alert)) # need to use print v return, as return will exit the function and thus terminate the while loop (i.e. will not query user for more keywords after initial prompt)
        # return "Top matches: %s \nLen Doc List: %s \nLen Score List: %s \nDoc List: %s \nScore List: %s \nSorted score %s" %(doc_list[:num_matches], len(doc_list), len(score_list), doc_list, score_list, sorted(score_list, reverse = True)) # for full results

        for doc_name in score_dict:
            score_dict[doc_name] = 0

## Test Dictionary
# print(top_n_matches({"a": "a b c d e", "b": "a b e h", "c": "i j k"}))

## Actual Dictionary ** print this for FINAL implementation of entire program **
# print(top_n_matches(get_all_texts(HOMEFOLDER)))

## Test Cases for top_n_matches (using Test Dictionary):
# Input: "a"; number of matches: 2 # correctly returns top 2 matches for a "(b,a)" according to scores
# Input: "2"; number of matches: 3 # correctly returns no matches (no scores > 0 as 2 is not in any of the documents)
# Input: "c"; number of matches: 1 # correctly returns 1 match and alerts user that there was only 1 match
# Input: "b"; number of matches: 5 # correctly returns 2 matches and alerts user that there were only 2 matches

## Test Cases for top_n_matches (using Actual Dictionary): after TF-IDF implementation (from Bells and Whistles, part 1), and after normalization (from Bells and Whistles, part 2)
# *note: there are only 5 documents in the entire filelist that include "parotid" as a word
# Input: "parotid"; number of matches: 2 # correctly returns top 2 matches for parotid
# Input: "parotid"; number of matches: 5 # correctly returns top 5 matches for parotid
# Input: "parotid"; number of matches: 7 # correctly returns top 5 matches and alerts user that there were only 5 matches

### *** End of Search Program - below are parts 4 and 5 of "Bells and Whistles" ***

# Part 4 - Write code to download all the infectious disease pages from Wikipedia (https://en.wikipedia.org/wiki/List_of_infectious_diseases)

# Plan:
# Option 1: extract hyperlink URLs of all files to download from from the list (specified URL), store name as keys, and URLs as values in dict, and use for loop to write a new file with the key as the name and the value as the contents (via a URLopen request). Whether this works will depend on the wiki source code, as it may not have HTML urls directly embedded, but truncated wiki URLs. If this is the case, try option 2.
# Option 2: analyze the embedded/wiki URL and break it down such that you construct the URL for each hyperlink URL in the list (specified URL); then key/dict as above.

#Since full URLs are not embedded in the source code, go with option 2.
# embedded URL structure: "/wiki/[name of infectious disease]""
# wiki URL structure: "https://en.wikipedia.org/wiki/[name of infectious disease]"

import urllib.request
import os

def download_infectious_diseases():
    os.chdir("/Users/nicolasahar/Desktop/")
    os.mkdir("List of Infectious Diseases") #use when first running the program
    os.chdir("/Users/nicolasahar/Desktop/List of Infectious Diseases")

    url = urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_infectious_diseases")

    f = open("list_of_infectious_diseases.txt", "w")
    f.write(url.read().decode("utf-8"))
    f.close()

    f = open("list_of_infectious_diseases.txt", "r+")
    file_list= [x.split() for x in f.readlines()]
    file_list1 = [x for sublist in file_list for x in sublist]
    f.close()

    wiki_dict = {} # dictionary of disease names and corresponding URLs
    error_dict = {}

    for word in file_list1:
        if word[:12] == "href=\"/wiki/":
            disease_name = word[12: word.find("\"", 12)] # word.find returns the index of the closing " in the embedded wiki URL; we want to capture everything after index 11 and upto the index returned by find (this gives us the disease name)

            if "Special" not in disease_name:
                wiki_dict[disease_name] = "https://en.wikipedia.org/wiki/%s" %(disease_name)

    os.mkdir("Downloaded Files")  # create new directory to house all of the downloaded files
    os.chdir("/Users/nicolasahar/Desktop/List of Infectious Diseases/Downloaded Files")

    for disease_name in wiki_dict:

        try:
            url = urllib.request.urlopen(wiki_dict[disease_name])
            f = open("%s.html" %(disease_name), "w")
            f.write(url.read().decode("utf-8"))
            f.close()

        except FileNotFoundError:
            error_dict[disease_name] = wiki_dict[disease_name]


    return error_dict #for some reason, python could not recognize the URLs for these links, even though they are valid and working links ({'HIV/AIDS': 'https://en.wikipedia.org/wiki/HIV/AIDS', 'Nasal_type_NK/T-cell_lymphoma': 'https://en.wikipedia.org/wiki/Nasal_type_NK/T-cell_lymphoma', 'Adult_T-cell_leukemia/lymphoma': 'https://en.wikipedia.org/wiki/Adult_T-cell_leukemia/lymphoma'})

print(download_infectious_diseases())


#Part 5 - Write code to download all the disease pages from https://en.wikipedia.org/wiki/Lists_of_diseases
import urllib.request
import os

def download_lists_of_diseases():
    os.chdir("/Users/nicolasahar/Desktop/")
    os.mkdir("Lists of Diseases") #use when first running the program
    os.chdir("/Users/nicolasahar/Desktop/Lists of Diseases")

    url = urllib.request.urlopen("https://en.wikipedia.org/wiki/Lists_of_diseases")

    f = open("list_of_diseases.txt", "w")
    f.write(url.read().decode("utf-8"))
    f.close()

    f = open("list_of_diseases.txt", "r+")
    file_list = [x.split() for x in f.readlines()]
    file_list1 = [x for sublist in file_list for x in sublist]
    f.close()

    wiki_dict = {}  # dictionary of disease names and corresponding URLs
    error_dict = {}

    #URL structure: href="/wiki/List_of_diseases_(X)" where X is the letter or number that the disease list starts with
    for word in file_list1:
        if word[:30] == "href=\"/wiki/List_of_diseases_(":
            list_name = word[12: word.find("\"", 12)]  # word.find returns the index of the closing " in the embedded wiki URL; we want to capture everything after index 11 and upto the index returned by find (this gives us the disease name)
            wiki_dict[list_name] = "https://en.wikipedia.org/wiki/%s" % (list_name)

    os.mkdir("List Name HTMLs")  # create new directory to house all of the downloaded files containing the lists of diseases
    os.chdir("/Users/nicolasahar/Desktop/Lists of Diseases/List Name HTMLs")

    for list_name in wiki_dict:
        try:
            url = urllib.request.urlopen(wiki_dict[list_name])
            f = open("%s.html" % (list_name), "w")
            f.write(url.read().decode("utf-8"))
            f.close()

        except FileNotFoundError:
            error_dict[disease_name] = wiki_dict[disease_name]

    # return wiki_dict

def download_diseases():

    import os
    rootdir = "/Users/nicolasahar/Desktop/Lists of Diseases/List Name HTMLs"

    for subdir, dirs, files in os.walk(rootdir): #loop through all of the files in the "List Name HTMLs" directory
        for file in files:
            f=open(file, "r+")
            file_list = [x.split() for x in f.readlines()]
            file_list1 = [x for sublist in file_list for x in sublist]
            f.close()

            wiki_dict = {}  # dictionary of disease names and corresponding URLs
            error_dict = {}

            for word in file_list1:
                if word[:12] == "href=\"/wiki/":
                    disease_name = word[12: word.find("\"",12)]  # word.find returns the index of the closing " in the embedded wiki URL; we want to capture everything after index 11 and upto the index returned by find (this gives us the disease name)
                    if "Special" not in disease_name:
                        wiki_dict[disease_name] = "https://en.wikipedia.org/wiki/%s" % (disease_name)

            os.chdir("/Users/nicolasahar/Desktop/Lists of Diseases/")
            os.mkdir(file[:-5])
            os.chdir("/Users/nicolasahar/Desktop/Lists of Diseases/%s" % (file[:-5])) # create new directory to house all of the downloaded files for each list of disease; cannot use "os.mkdir(file[:-5])" to refer to new file as it returns None; file[:-5] returns the filename (as it returns as string)

            for disease_name in wiki_dict:
                try:
                    url = urllib.request.urlopen(wiki_dict[disease_name])
                    f = open("%s.html" % (disease_name), "w")
                    f.write(url.read().decode("utf-8"))
                    f.close()

                except FileNotFoundError:
                    error_dict[disease_name] = wiki_dict[disease_name]

            # print(error_dict)

print(download_lists_of_diseases())
print(download_diseases())

# Next steps for part 4 and 5 - remove downloads that are not diseases (e.g. main page, List of Disease, About)
