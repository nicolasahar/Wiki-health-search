# Here are a few very simple tests to run on your functions to ensure that they
# have the signatures that we specified. (A signature of a function is the
# type and order of the parameters and also the type of the returned value.)
#
# These basic tests do NOT thoroughly test your code. Do that yourself.
# They provide a confirmation that your understanding of the types of each
# parameter was correct. If one of your functions does not pass one of these 
# tests or does not even complete, then something is wrong and you should 
# come to office hours before submitting your solution.
#
# Only the first two tests specify the output. For the next five, you'll need
# to read the input and work out the output that you should be expecting.
#
################################################################################

import math
import os

#Testing keyword_found
#


def keyword_found(keyword, doc_name, disease_to_text):
    """ (str, str, dict of {str:str}) -> bool

    Return True iff keyword is found in this doc_name inside disease_to_text
    as a full token separated by whitespace.

    """
    if keyword in disease_to_text[doc_name].split(): #Note: don't need to worry about punctuation in the tokens as it has all been removed!
        return True
    else:
        return False

#sample dictionary
docs = {"doc1": "mykeywords mykeywords", "doc2": "mykeyword mykeyword"}

actual   = keyword_found("mykeyword", "doc1", docs)
expected = False 
print("TEST 1 output:", actual, "\tTEST 1 expected:", expected, "\tPASSED?", actual == expected)


actual   = keyword_found("mykeyword", "doc2", docs)
expected = True 
print("TEST 2 output:", actual, "\tTEST 2 expected:", expected, "\tPASSED?", actual == expected)


################################################################################
#Test idf

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

#sample dictionary
docs = {"doc1": "a b c", "doc2": "c d f", "doc3": "g e h"}

actual = idf("z", docs)
print("TEST 3 output:", actual)

actual = idf("a", docs)
print("TEST 4 output:", actual)

actual = idf("c", docs)
print("TEST 5 output:", actual)



################################################################################
#Test build_empty_scores_dict

def build_empty_scores_dict(disease_to_text):
    """ (dict of {str:str}) -> dict of {str:number}
    Build and return an empty dictionary where the keys are the same as the keys in disease_to_text
    and the values are all 0.
    """

    current_scores = {}

    for doc_name in disease_to_text:
        current_scores[doc_name] = 0

    return current_scores

docs = {"doc1": "a b c", "doc2": "c d f", "doc3": "g e h"}
actual = build_empty_scores_dict(docs)
print("TEST 6 output:", actual)

################################################################################
#Test update_scores

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
                current_scores[doc_name] += score

    return current_scores

docs = {"doc1": "a b c", "doc2": "c d f", "doc3": "g e h"}
scores = {"doc1": 0, "doc2": 0, "doc3": 0}
update_scores(scores, "c", docs)
print("TEST 7 output:", scores)

