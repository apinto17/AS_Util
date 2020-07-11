import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support


pc = "Safety"
data_file = "categories_cleaned_big_5_in_per_out.csv"


def train_model():

    data = pd.read_csv(data_file)

    train = data.sample(frac=0.9,random_state=200)
    test = data.drop(train.index)

    svm = LinearSVC(random_state=0, max_iter=10000, C=.4)
    clf = CalibratedClassifierCV(svm)
    vect = CountVectorizer(ngram_range=(1,2))
    pipeline = Pipeline([
            ("vect", vect),
            ("clf", clf)
    ])

    y_pred = pipeline.fit(train["cleaned"], train["output_category"]).predict(test["cleaned"])

    accur = accuracy_score(test['output_category'], y_pred)
    scores = precision_recall_fscore_support(test['output_category'], y_pred)

    print("\n\n----------------LINEAR_SVC-----------------")

    print("\n\n" + data_file)

    for score in scores:
        print("Precision: " + str(score[0]))
        print("Recall: " + str(score[1]))
        print("F1: " + str(score[2]))
        print()

    print("Accuracy:" + str(accur) + "\n\n")

    print("---------EXPECTED------------")
    print(list(test["output_category"]))
    print("--------ACTUAL------------")
    print(y_pred)

    


def run_categorizer():

    model, data = train_model()
    res = []
    new_session_I_C = Select_Input_Cat_From_DB(pc)
    for x in new_session_I_C:
        cat_string = x[0]
        if(len(selections) > NUM_AUTO_SAVE):
            save()
        print("---------------------------------------------------------")
        print("Enter category string or type \'exit\' to save and exit ")
        print("type \'s\' to skip and \'f\' to add five more")
        print('Categorize the following:', cat_string)

        get_suggestions(cat_string, data, model)


def get_suggestions(cat_string, data, model):

    best_n_indx = 0
    res_num = 1
    res = []

    # grab initial data
    res.append((res_num, str(model.predict([cat_string])), "Unknown"))
    res_num += 1
    probs = model.predict_proba([cat_string])
    probs = probs.flatten()
    best_n = np.argsort(probs)[::-1]

    res, best_n_indx, res_num, selection = display_data(res, best_n, probs, best_n_indx, res_num, data)

    # if user printed 5 more
    while(type(selection) is str and selection == "f"):
        res, best_n_indx, res_num, selection = display_data(res, best_n, probs, best_n_indx, res_num, data)

    append_selection(cat_string, selection, res)


def display_data(res, best_n, probs, best_n_indx, res_num, data):

    limit = 0
    if best_n_indx == 0:
        limit = NUM_SUG - 1
    elif(len(best_n) <= (best_n_indx + NUM_SUG)):
        limit = len(best_n) - (best_n_indx + NUM_SUG)
    else:
        limit = NUM_SUG

    for i in range(limit):
        res.append((res_num, data["output_unique"].iloc[best_n[best_n_indx]],probs[best_n[best_n_indx]]))
        best_n_indx += 1
        res_num += 1

    print_res(res, res_num)
    selection = handle_input()

    return (res, best_n_indx, res_num, selection)


def append_selection(cat_string, selection, res):

    global selections
    global cat_strings

    if(type(selection) is int and selection > 0 and selection <= NUM_CATS):
        print("You Selected \"" + res[selection - 1][1] + "\"")
        selections.append(res[selection - 1][1])
        cat_strings.append(cat_string)


def handle_input():
    selection = input()
    selection = selection.lower()
    if(selection == "exit"):
        save_and_exit()
    elif(selection.isdigit()):
        selection = int(selection)
    return selection



def print_res(res, res_num):
    for i in range(-NUM_SUG + res_num - 1, res_num - 1):
        if(type(res[i][2]) is not str):
            print("          (" + str(res[i][0]) + ") " + str(res[i][1]) + "     Accuracy: %.2f%%" % (float(res[i][2]) * 100))
        else:
            print("          (" + str(res[i][0]) + ") " + str(res[i][1]) + "     Accuracy: " + res[i][2])


def save_and_exit():
    print("#########  EXITING: Writing results to \'selections.xlsx\'  #################")
    print(cat_strings)
    print(selections)

    global server

    df = pd.DataFrame({'input' : cat_strings,
                        'output' : selections})

    writer = pd.ExcelWriter("selections.xlsx", engine='openpyxl')
    df.to_excel(writer, "Sheet1")
    writer.save()
    del server
    exit()

def save():

    print("#########  AUTO SAVE: Writing results to \'selections.xlsx\'  #################")

    print(cat_strings)
    print(selections)

    df = pd.DataFrame({'input' : cat_strings,
                        'output' : selections})

    writer = pd.ExcelWriter("selections.xlsx", engine='openpyxl')
    df.to_excel(writer, "Sheet1")
    writer.save()


# DEAD CODE maybe used in the future?
def append_df_to_excel(filename, df, sheet_name='Sheet1', startrow=None,
                       truncate_sheet=False,
                       **to_excel_kwargs):
    """
    Append a DataFrame [df] to existing Excel file [filename]
    into [sheet_name] Sheet.
    If [filename] doesn't exist, then this function will create it.

    Parameters:
      filename : File path or existing ExcelWriter
                 (Example: '/path/to/file.xlsx')
      df : dataframe to save to workbook
      sheet_name : Name of sheet which will contain DataFrame.
                   (default: 'Sheet1')
      startrow : upper left cell row to dump data frame.
                 Per default (startrow=None) calculate the last row
                 in the existing DF and write to the next row...
      truncate_sheet : truncate (remove and recreate) [sheet_name]
                       before writing DataFrame to Excel file
      to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel()`
                        [can be dictionary]

    Returns: None
    """

    # ignore [engine] parameter if it was passed
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    writer = pd.ExcelWriter(filename, engine='openpyxl')

    try:
        # try to open an existing workbook
        writer.book = load_workbook(filename)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)

        # copy existing sheets
        writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        # file does not exist yet, we will create it
        pass

    if startrow is None:
        startrow = 0

    # write out the new sheet
    df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

    # save the workbook
    writer.save()


def get_wb():

    book = None
    fname = "selections.xlsx"
    if os.path.isfile(fname):
        book=load_workbook(fname)
    else:
        workbook2=xlwt.Workbook(fname)
        ws = workbook2.add_sheet('Sheet1')
        workbook2.save(fname)
        book = open_workbook(fname)

    return book


def Select_Input_Cat_From_DB(pc):
    #new session/raw input_category data that only has the primary category the user selected

    ri = []
    df = pd.read_csv("categories_cleaned_small.csv")
    #for index, row in df.iterrows():
        #i_c_test = ri.append(row['input_category'])
    #print(ri)
    
                                                        #returns each row as a tuple
    # for row in df.itertuples(index=False,name=None): 
    #     if row[0] == pc:                                #need to use index
    #         #i_c = ri.append(row[1])                     #need to use index
    #         ri.append((row[1],)) #added (,)
    #         #print(row)
    #         #print(ri)
    #         returned_items = ri
    #     else:
    #         pass

    return df


def Select_Training_Data_From_DB(pc):
     #input & output_category training data that only has the primary category the user selected

    input_categories = []
    output_categories = []
    df = pd.read_excel('categorizer_data_TW.xlsx', sheet_name='training_data')
    for index, row in df.iterrows():
        if row['primary_category'] == pc:
            i_c = input_categories.append(row['input_category'])
            o_c = output_categories.append(row['output_category'])
        else:
            pass
    #print(len(input_categories))
    #print(len(output_categories))

    # input_categories = []
    # output_categories = []
    # for cat in returned_items:
    #     input_categories.append(cat[0])
    #     output_categories.append(cat[1])

    return (input_categories, output_categories)


def Select_Unique_Output_Cat_From_DB(pc):
#unique output_cats for training model
    #self.connect()

    output_unique_list = []
    df = pd.read_excel('categorizer_data_TW.xlsx', sheet_name='distinct_output_category')
    for index, row in df.iterrows():
        #testx = row['primary_category']
        #print(testx)
        if row['primary_category'] == pc:
            o_c = output_unique_list.append(row['d_oc'])
            output_unique = output_unique_list
        else:
            pass

    #print(output_unique)
    return output_unique    

    # output_unique = list(self.mycursor.fetchall())
    # self.connection.close()

   #print([out[0] for out in output_unique])
    #return [out[0] for out in output_unique]


if(__name__ == "__main__"):
    # try:
    #     if(len(sys.argv) == 2):
    #         globals()[sys.argv[1]]()
    #     elif(len(sys.argv) == 3):
    #         globals()[sys.argv[1]](sys.argv[2])
    #     else:
    #         print("Usage: python categorizer.py method_name [args]")
    #         print("method_names:")
    #         print("     run_categorizer")
    #         print("     pickle_model")
    # except KeyboardInterrupt:
    #     save_and_exit()
    #     try:
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)
    train_model()
