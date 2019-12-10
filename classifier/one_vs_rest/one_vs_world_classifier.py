import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import re
from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.calibration import CalibratedClassifierCV
import json
from data_explore import clean


# TODO try a random forrest or decision tree classifier
# TODO get more data for a more clean train-test split

def main():
    svm = LinearSVC(random_state=0, max_iter=10000, C=.4)
    clf = CalibratedClassifierCV(svm)
    vect = CountVectorizer(ngram_range=(1,2))
    pipeline = Pipeline([
            ("vect", vect),
            ("clf", clf)
    ])
    data_file = open("categories.json", "r+")
    data = json.load(data_file)

    data = pd.DataFrame({'input_category' : data["input_categories"],
                        'output_category' : data["output_categories"]})

    data = clean(data)

    train_indx = int((.7 * len(data)))

    train = data[:train_indx]
    test = data[train_indx:]
    print(OneVsRestClassifier(pipeline).fit(train["cleaned"], train["output_category"]).predict(test['cleaned']))


    # x_train, x_test, y_train, y_test = train_test_split(data["input_category"], data["cleaned"], test_size=.3)

    # print(OneVsRestClassifier(pipeline).fit(x_train, y_train).predict(x_test))








if (__name__ == "__main__"):
    main()
