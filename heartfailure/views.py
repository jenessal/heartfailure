from flask import render_template, jsonify, request
from copy import copy

import pandas as pd

from heartfailure import app
from heartfailure.models import train, download_data

global MODELS
MODELS = {}


@app.route('/train', methods=['GET'])
def train_point():
    """API entry point for to kick off the training."""
    global MODELS

    ret = train()
    models = pd.Series(ret.keys()).to_dict()
    MODELS = copy(ret)
    return jsonify(models)


@app.route('/predict', methods=['POST'])
def predict():
    """API entry point to request a prediction."""
    global MODELS
    _, _, columns = download_data()
    data = request.json

    # If an data point is missing we fill in a 0.
    x = pd.Series(data).reindex(columns).fillna(0.).values

    ret = {}
    for label, model in MODELS.items():
        ret[label] = int(model.predict([x])[0])

    return jsonify(ret)