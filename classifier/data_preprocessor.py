import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

def main():

    MIN_ROWS = 5
    stemmer = SnowballStemmer("english")
    words = stopwords.words("english")

    data = pd.read_csv("categories_small.csv")
    #data = duplicate_rows(data, MIN_ROWS)

    data["cleaned"] = data["input_category"].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

    data.to_csv("categories_cleaned_small.csv")


def duplicate_rows(data, min_rows):

    len_so_far = 0
    i = 0
    while(i < len(data["output_category"])):
        if(i > 0 and data["output_category"][i] != data["output_category"][i-1]):
            if(len_so_far < min_rows):
                for j in range(min_rows - len_so_far):
                    data = insert_row(i, data, data.iloc[i-1])
                    i += 1
            len_so_far = 0
        else:
            len_so_far += 1

        i += 1

    return data


def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]

    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)

    return df


if __name__ == "__main__":
    main()
