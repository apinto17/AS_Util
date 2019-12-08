import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import StandardScaler

def main():

    print("reading data...")
    # read data and remove duplicates from output column
    data = pd.read_excel("grainger_cleaned_w_dups.xlsx")

    pipeline = Pipeline([
            ("vect", CountVectorizer(ngram_range=(1,2))),
            ("clf", LinearSVC(random_state=0, max_iter=10000))
    ])

    grid = {
            "clf__C":[.8, .6, .5, .4, .3, .2],
            "clf__dual":[True, False]
            }
    print("tuning...")
    grid_search = GridSearchCV(estimator=pipeline, param_grid=grid, scoring="accuracy", n_jobs=-1, cv=5)
    grid_search.fit(X=data["cleaned"], y=data["Output"])

    print("________Results________")
    print(grid_search.best_score_)
    print(grid_search.best_params_)

if(__name__ == "__main__"):
    main()
