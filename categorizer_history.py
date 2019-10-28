import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.base import TransformerMixin

def main():

    # pre-processing (minimal)

    data = pd.read_excel("grainger_category_data.xlsx")

    x_train, x_test, y_train, y_test = train_test_split(data["Input"], data.Output, test_size=.2)


    # training models
    print("bulding and training...")

    # pipe_trans_gnb = Pipeline([("vect", TfidfVectorizer()), ('to_dense', DenseTransformer()), ("clf", GaussianNB())])
    # pipe_hash_gnb = Pipeline([("vect", HashingVectorizer()), ('to_dense', DenseTransformer()), ("clf", GaussianNB())])

    pipe_trans = Pipeline([("vect", TfidfVectorizer()), ("clf", LinearSVC(random_state=0))])
    pipe_hash = Pipeline([("vect", HashingVectorizer()), ("clf", LinearSVC(random_state=0))])

    # model_trans_gnb = pipe_trans_gnb.fit(x_train, y_train)
    # model_hash_gnb = pipe_hash_gnb.fit(x_train, y_train)

    model_trans = pipe_trans.fit(x_train, y_train)
    model_hash = pipe_hash.fit(x_train, y_train)

    # results

    print("LinearSVC trans model accuracy score: " + str(model_trans.score(x_test, y_test)))
    print("LinearSVC hash model accuracy score: " + str(model_hash.score(x_test, y_test)))

    # TODO test GNB model
    # print("GNB trans model accuracy score: " + str(model_trans_gnb.score(x_test, y_test)))
    # print("GNB hash model accuracy score: " + str(model_hash_gnb.score(x_test, y_test)))

    # RESULT : LinearSVC hash model is best (TODO test GNB)

    ############## to verify output ###############
    # # Output
    # print("___________Actual prediction from other site______________")
    # print("difficult:")
    # print("Actual:")
    # print(model.predict(["Adhesives and Sealants|Dispensers & Application Equip.|Adhesive & Sealant Guns & Applicators"]))
    # print("Expected:")
    # print("Adhesive Dispensing Equipment\n\n")
    # print("easy:")
    # print("Actual:")
    # print(model.predict(["Abrasives|Abrasive Brushes|Abrasive Brush Accessories"]))
    # print("Expected:")
    # print("Abrasive Brushes and Wheel Kits")


    # vectorizer = model.named_steps["vect"]
    # chi = model.named_steps["chi"]
    # clf = model.named_steps["clf"]
    #
    # feature_names = vectorizer.get_feature_names()
    # feature_names = [feature_names[i] for i in chi.get_support(indices=True)]
    # feature_names = np.asarray(feature_names)
    #
    # target_names = ["Relays and Accessories", "Tapes", "Plugs and Connectors", "Wire Connectors"]
    # print("top key words")
    # for i, label in enumerate(target_names):
    #         top10 = np.argsort(clf.coef_[i][-10:])
    #         print("%s: %s" % (label, " ".join(feature_names[top10])))
    #
    # print("accuracy score: " + str(model.score(X_test, Y_test)))


class DenseTransformer(TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None, **fit_params):
        return X.todense()



if(__name__ == "__main__"):
    main()
