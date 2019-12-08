import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = None
stop_words = None

def preprocess_data(data):

    global lemmatizer
    global stop_words

    # define lemmatizer and stop words
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")

    # clean data
    return data.apply(process_row)


def process_row(input):

    tokens = input.split("|")
    res = []
    for token in tokens:
        res.append(process_token(token))

    return "|".join(res)



def process_token(token):

    global lemmatizer
    global stop_words

    res = []
    line = token.split(" ")
    for word in line:
        word = re.sub("[^a-zA-Z]", "", word).lower()
        if word not in stop_words and word is not "":
            res.append(lemmatizer.lemmatize(word))

    return " ".join(res)
