from flask import render_template, jsonify, request
from copy import copy

import pandas as pd
from joblib import dump, load

from heartfailure import app
from heartfailure.models import train, load_data

global MODELS
MODELS = {}
global COLS
COLS = []

DATA_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/00519/heart_failure_clinical_records_dataset.csv"
TARGET_VARIABLE = 'DEATH_EVENT'


@app.route('/train', methods=['GET'])
def train_point():
    """API entry point for to kick off the training."""
    global MODELS
    global COLS

    url = request.args.get('url', default=DATA_URL, type=str)
    target_variable = request.args.get('url',
                                       default=TARGET_VARIABLE,
                                       type=str)
    trained_models, cols = train(url=url, target_var=target_variable)
    models = pd.Series(trained_models.keys()).to_dict()

    COLS = cols
    MODELS = copy(trained_models)

    return jsonify(models)


@app.route('/predict', methods=['POST'])
def predict():
    """API entry point to request a prediction."""
    global MODELS
    global COLS
    data = request.json

    x = pd.Series(data).reindex(COLS).values

    predictions = {}
    for label, model in MODELS.items():
        predictions[label] = int(model.predict([x])[0])

    return jsonify(predictions)