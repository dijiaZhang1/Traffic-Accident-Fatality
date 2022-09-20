from flask import Flask, request, jsonify
import traceback
import pandas as pd
import joblib
import sys
from os import path
from sklearn import metrics
from flask_cors import CORS
import numpy as np

models = {
    "Logistic_Regression": "lr_fullpipe_feng.pkl",
    "SVM": "svm_fullpipe_zhang.pkl",
    "Decision_Tree": "tree_fullpipe_hernandez.pkl"
}
model_columns = None

x_train = pd.read_csv('x_train_data.csv', index_col=0)
y_train = pd.read_csv('y_train_data.csv', index_col=0)
x_test = pd.read_csv('x_test_data.csv', index_col=0)
y_test = pd.read_csv('y_test_data.csv', index_col=0)

app = Flask(__name__)
CORS(app)


# use decorator pattern for the route
@app.route("/predict/<model_name>", methods=['GET', 'POST'])
def predict(model_name):
    if loaded_model:
        try:
            model_json = request.json
            query = pd.DataFrame(model_json, index=[0])
            print(query)
            prediction = list(loaded_model[model_name].predict(query))
            print(f'Returning prediction with {model_name} model:')
            print('prediction=', prediction)
            print('JSON:\n', model_json)
            res = jsonify({"prediction": str(prediction)})
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        return ('No model found')


# use decorator pattern for the route
@app.route("/scores/<model_name>", methods=['GET', 'POST'])
def scores(model_name):
    if loaded_model:
        try:
            y_pred = loaded_model[model_name].predict(x_test)
            print(f'Returning scores for {model_name}:')
            accuracy = metrics.accuracy_score(y_test, y_pred)
            precision = metrics.precision_score(y_test, y_pred)
            recall = metrics.recall_score(y_test, y_pred)
            f1 = metrics.f1_score(y_test, y_pred)
            print(
                f'accuracy={accuracy}  precision={precision}  recall={recall}  f1={f1}')
            res = jsonify({"accuracy": accuracy,
                           "precision": precision,
                           "recall": recall,
                           "f1": f1
                           })
            res.headers.add('Access-Control-Allow-Origin', '*')
            return res
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        return ('No model available.')


@app.route("/cat_attribute", methods=['GET'])
def attribute():
    cat_columns = x_test.select_dtypes(exclude=[np.number]).columns
    categoricalData = x_test[cat_columns]
    res = {}
    for col in categoricalData:
        res[col] = categoricalData[col].unique().tolist()
    return jsonify(res)


@app.route("/sample", methods=['GET'])
def sample():
    try:
        res = x_test.head(5).to_json(orient='records')
        return res
    except:
        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])  # This is for a command-line input
    except:
        port = 12345  # If you don't provide any port the port will be set to 12345

    # # load all models:
    loaded_model = {}
    for model_name in (models):
        loaded_model[model_name] = joblib.load(
            path.join(models[model_name]))
        print(f'Model {model_name} loaded')

    # model_columns = x_train.columns
    # query = {"ACCNUM": 1300176, "YEAR": 2012, "TIME": 2016, "HOUR": 20, "ROAD_CLASS": "Minor Arterial", "DISTRICT": "Toronto and East York", "LATITUDE": 43.643445, "LONGITUDE": -79.43779, "LOCCOORD": "Mid-Block", "ACCLOC": "Other", "TRAFFCTL": "No Control", "VISIBILITY": "Rain", "LIGHT": "Dusk, artificial", "RDSFCOND": "Wet", "IMPACTYPE": "Pedestrian Collisions",
    #          "INVTYPE": "Driver", "INVAGE": "30 to 34", "VEHTYPE": "Automobile, Station Wagon", "PEDESTRIAN": "Yes", "CYCLIST": "No", "AUTOMOBILE": "Yes", "MOTORCYCLE": "No", "TRUCK": "No", "TRSN_CITY_VEH": "No", "EMERG_VEH": "No", "PASSENGER": "No", "SPEEDING": "No", "AG_DRIV": "Yes", "REDLIGHT": "No", "ALCOHOL": "No", "DISABILITY": "No", "HOOD_ID": 86, "WEEKDAY": 3, "DAY": 21, "MONTH": 6}
    # prediction = loaded_model['SVM'].predict(pd.DataFrame(query, index=[0]))
    # print(prediction)
app.run(port=port, debug=True)
