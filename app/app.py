from flask import Flask, render_template, jsonify, request
import pickle
import pandas as pd
import datetime

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold

# import machine learning model pickle file
with open('model/mushroom_classifier.pkl', 'rb') as f:
    rfc = pickle.load(f)

mushrooms = pd.read_csv('data/mushrooms_encoded.csv')


# search data set for all records with matching characteristics
def mushrooms_match(data):
    gill_color = data['gillColor']
    spore_print_color = data['sporePrintColor']
    population = data['population']
    gill_size = data['gillSize']
    matched = []

    match1 = len(mushrooms.loc[(mushrooms['gill-color'] == gill_color)])
    match2 = len(mushrooms.loc[(mushrooms['spore-print-color'] == spore_print_color)])
    match3 = len(mushrooms.loc[(mushrooms['population'] == population)])
    match4 = len(mushrooms.loc[(mushrooms['gill-size'] == gill_size)])

    matched.append(match1)
    matched.append(match2)
    matched.append(match3)
    matched.append(match4)

    print(matched)

    return matched


# search data set for edible records with matching characteristics
def mushrooms_edible(data):
    gill_color = data['gillColor']
    spore_print_color = data['sporePrintColor']
    population = data['population']
    gill_size = data['gillSize']
    edible = []

    edible1 = len(mushrooms.loc[(mushrooms['class'] == 0) & (mushrooms['gill-color'] == gill_color)])
    edible2 = len(mushrooms.loc[(mushrooms['class'] == 0) & (mushrooms['spore-print-color'] == spore_print_color)])
    edible3 = len(mushrooms.loc[(mushrooms['class'] == 0) & (mushrooms['population'] == population)])
    edible4 = len(mushrooms.loc[(mushrooms['class'] == 0) & (mushrooms['gill-size'] == gill_size)])

    edible.append(edible1)
    edible.append(edible2)
    edible.append(edible3)
    edible.append(edible4)

    print('Edible', edible)
    return edible


# search data set for poisonous records with matching characteristics
def mushrooms_poisonous(data):
    gill_color = data['gillColor']
    spore_print_color = data['sporePrintColor']
    population = data['population']
    gill_size = data['gillSize']
    poisonous = []

    poisonous1 = len(mushrooms.loc[(mushrooms['class'] == 1) & (mushrooms['gill-color'] == gill_color)])
    poisonous2 = len(mushrooms.loc[(mushrooms['class'] == 1) & (mushrooms['spore-print-color'] == spore_print_color)])
    poisonous3 = len(mushrooms.loc[(mushrooms['class'] == 1) & (mushrooms['population'] == population)])
    poisonous4 = len(mushrooms.loc[(mushrooms['class'] == 1) & (mushrooms['gill-size'] == gill_size)])

    poisonous.append(poisonous1)
    poisonous.append(poisonous2)
    poisonous.append(poisonous3)
    poisonous.append(poisonous4)

    print('Poisonous', poisonous)
    return poisonous


# classify request data
def classify(data):
    prediction = rfc.predict([data])[0]

    if prediction == 1:
        result = 'Poisonous'
    elif prediction == 0:
        result = 'Edible'
    else:
        result = 'Error'
    return result


# parse and validate request data
def data_prep(data):
    gill_color = data['gillColor']
    spore_print_color = data['sporePrintColor']
    population = data['population']
    gill_size = data['gillSize']

    new_data = [gill_color, spore_print_color, population, gill_size]

    invalid_data = False

    # check for incorrect number of values
    if len(new_data) != 4:
        invalid_data = True
    else:
        # check to make sure all values are integers
        for value in new_data:
            try:
                int(value)
            except ValueError:
                invalid_data = True
        # check to make sure values are within set range
        for value in new_data:
            if value < 0 or value > 11:
                invalid_data = True
    # return empty list if data is invalid
    if invalid_data:
        new_data = []

    return new_data


app = Flask(__name__)


# index page
@app.route('/')
def index():
    return render_template('index.html')


# classify api
@app.route('/classify', methods=['GET', 'POST'])
def get_result():
    if request.method == 'GET':
        return jsonify(result='Error')

    # receive data from post request
    if request.method == 'POST':
        data = request.json

        # parse post request data
        new_data = data_prep(data)

        # log error if request data is invalid
        if len(new_data) == 0:
            result = 'Error'
            ts = datetime.datetime.now()
            log_file = open('log/errors.txt', 'a')  # append mode
            log_file.write(str(ts) + '\n' + str(data) + '\n')
            log_file.close()

        # classify request data if valid
        else:
            result = classify(new_data)

        matched = mushrooms_match(data)
        edible = mushrooms_edible(data)
        poisonous = mushrooms_poisonous(data)

        # return results to dashboard
        return jsonify(result=result, matched=matched, edible=edible, poisonous=poisonous)


# about page
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=8000)
