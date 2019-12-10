import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
import mysql.connector
import sshtunnel


NUM_PER_OUTPUT = 10



def main():
    server = Server()
    data = server.select_item_data()
    data = pd.DataFrame(data)
    data.to_csv("item_data.csv")
    del server


def display():
    data_file = open("categories.json", "r+")
    data = json.load(data_file)

    data = pd.DataFrame({'input_category' : data["input_categories"],
                        'output_category' : data["output_categories"]})

    data = clean(data)

    cats_so_far = {}
    for i in range(len(data)):
        if(data['output_category'].iloc[i] in cats_so_far.keys()):
            cats_so_far[data['output_category'].iloc[i]].append(data['cleaned'].iloc[i])
        else:
            cats_so_far[data['output_category'].iloc[i]] = []

    print("------------after---------------")
    for k, v in cats_so_far.items():
        print("")
        print(k + ": " + str(v) + "\n\n\n")






def clean(data):
    stemmer = SnowballStemmer("english")
    words = stopwords.words("english")
    indexes = []

    for i in range(len(data)):
        if(len(data[data['output_category'] == data['output_category'].iloc[i]]) < NUM_PER_OUTPUT):
            new_indexes = get_occurences(data, data['output_category'].iloc[i], indexes)
            indexes.extend(new_indexes)

    for i in indexes:
        data = data.drop(i)

    data["cleaned"] = data["input_category"].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())


    return data


def get_occurences(data, item, indexes_so_far):
    indexes = []
    for i in range(len(data)):
        if(data['output_category'].iloc[i] == item and i not in indexes_so_far):
            indexes.append(i)

    return indexes



# sql queries only work on windows for some reason
class Server:
    server = None
    connection = None
    mycursor = None

    def __init__(self):
        sshtunnel.SSH_TIMEOUT = 350.0
        sshtunnel.TUNNEL_TIMEOUT = 350.0
        self.server = sshtunnel.SSHTunnelForwarder(
            ('ssh.pythonanywhere.com'),
            ssh_username='iclam19', ssh_password='@astest@1234',
            remote_bind_address=('iclam19.mysql.pythonanywhere-services.com', 3306)
        )
        self.server.start()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user='iclam19', password='astest1234',
                host='127.0.0.1', port=self.server.local_bind_port,
                database='iclam19$AssembledSupply',
            )
            if(self.connection.is_connected()):
                self.mycursor = self.connection.cursor()
            else:
                print("Did not connect")
                return None

        except Error as e:
            print(e)


    def __del__(self):
        self.server.stop()


    def Select_Training_Data_From_DB(self):
         #new session input & output_category data that only has the primary category the user selected
        self.connect()

        sql = "Select input_category, output_category From ft_ml_categories Where output_category is not null"

        self.mycursor.execute(sql,)
        returned_items = list(self.mycursor.fetchall())
        self.connection.close()

        input_categories = []
        output_categories = []
        for cat in returned_items:
            input_categories.append(cat[0])
            output_categories.append(cat[1])

        return (input_categories, output_categories)



    def select_item_data(self):
        self.connect()
        sql = "select item_description, price, category, site_name from ft_crawled_data limit 1000;"

        self.mycursor.execute(sql,)
        returned_items = list(self.mycursor.fetchall())
        self.connection.close()

        return returned_items







if(__name__ == "__main__"):
    main()
