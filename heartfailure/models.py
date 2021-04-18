import functools

import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.svm import LinearSVC


@functools.lru_cache()
def download_data() -> tuple:
    """Downloads the data set and extracts features, class labels and feature names."""
    link = "http://archive.ics.uci.edu/ml/machine-learning-databases/00519/heart_failure_clinical_records_dataset.csv"
    ret = pd.read_csv(link)

    columns = ret.iloc[:, :-1].columns
    X = ret.iloc[:, :-1].values
    y = ret.iloc[:, -1].values
    return X, y, columns


@functools.lru_cache()
def train() -> dict:
    """Trains all models defined below on the data set."""
    X, y, _ = download_data()
    ret = {}

    models = [
        ("LR",
         make_pipeline(
             StandardScaler(),
             LogisticRegressionCV(cv=3, random_state=0),
         )),
        ("KN",
         make_pipeline(
             StandardScaler(),
             KNeighborsClassifier(n_neighbors=3),
         )),
        ("SVM",
         make_pipeline(
             StandardScaler(),
             LinearSVC(random_state=0, tol=1e-05),
         )),
    ]

    for label, model in models:
        x = model.fit(X, y)
        ret[label] = x
    return ret