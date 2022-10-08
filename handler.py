import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.rossmann import Rossmann
import os

# Loading model
model = pickle.load(open('/model/model_rossmann.pkl', 'rb'))

# Initialize API
app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()

    if test_json:
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0]) # Only one example
        else:
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys()) # Multiple examples

        # Instantiate Rossmann Class
        pipeline = Rossmann()

        # Data Cleaning
        df1 = pipeline.data_cleaning(test_raw)

        # Feature Engineering
        df2 = pipeline.feature_engineering(df1)

        # Data Preparation
        df3 = pipeline.data_preparation(df2)

        # Prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response

    else:
        return Response('{}', status=200, minetype='application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='10.0.0.102', port=port)
