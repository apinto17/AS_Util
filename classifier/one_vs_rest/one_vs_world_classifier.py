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
from data_explore import *
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
# import sshtunnel
# import mysql.connector


def main():
    svm = LinearSVC(random_state=0, max_iter=10000, C=.4)
    clf = CalibratedClassifierCV(svm)
    vect = CountVectorizer(ngram_range=(1,2))
    pipeline = Pipeline([
            ("vect", vect),
            ("clf", clf)
    ])
    data = pd.read_csv("categories_cleaned_small.csv")
    train = data.sample(frac=0.8,random_state=200)
    test = data.drop(train.index)

    y_pred = OneVsRestClassifier(pipeline).fit(train["cleaned"], train["output_category"]).predict(test['cleaned'])

    accur = accuracy_score(test['output_category'], y_pred)
    scores = precision_recall_fscore_support(test['output_category'], y_pred)

    for score in scores:
        print("Precision: " + str(score[0]))
        print("Recall: " + str(score[1]))
        print("F1: " + str(score[2]))
        print()

    print("Accuracy:" + str(accur) + "\n\n")

    print("---------INPUT------------")
    print(list(test["output_category"]))
    print("--------OUTPUT------------")
    print(y_pred)





if (__name__ == "__main__"):
    main()
