import functools

import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier


@functools.lru_cache()
def load_data(url: str, target_var: str) -> tuple:
    """Downloads the dataset from given url and extracts features, class labels and feature names."""
    # link = "http://archive.ics.uci.edu/ml/machine-learning-databases/00519/heart_failure_clinical_records_dataset.csv"
    data = pd.read_csv(url)

    X = data.copy()
    y = X.pop(target_var)
    columns = X.columns
    return X.values, y.values, columns


@functools.lru_cache()
def train(url: str, target_var: str) -> dict:
    """Trains all models defined below on the data set."""
    X, y, cols = load_data(url, target_var)
    trained_models = {}

    def _pipeline(model):
        return make_pipeline(
            StandardScaler(),
            model,
        )

    models = [
        ("LR",
         _pipeline(
             LogisticRegressionCV(
                 cv=5,
                 random_state=0,
                 class_weight='balanced',
             ))),
        ("GB", _pipeline(GradientBoostingClassifier())),
        ("NN",
         _pipeline(
             MLPClassifier(
                 max_iter=1000,
                 hidden_layer_sizes=(8, 8, 4, 4),
                 activation='tanh',
                 learning_rate_init=0.005,
             ))),
    ]

    for label, model in models:
        x = model.fit(X, y)
        trained_models[label] = x

    clf = VotingClassifier(estimators=list(trained_models.items()),
                           voting='soft')
    clf.fit(X, y)
    trained_models['ensemble'] = clf
    return trained_models, cols