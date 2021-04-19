# heartfailure

The package structure is based on <https://github.com/candidtim/cookiecutter-flask-minimal> which is a very simple Python package scaffold for Flask APIs. I used cookiecutter and modified it slightly to fit the application.

## Run API Server

The package requires Python 3.7, `make` and the python package `virtualenv` to build a virtual environment from which to run the server. To get a Python 3.7 environment for example with `conda` we can run `conda create -n myenv python=3.7`, `conda activate myenv` and `pip install virtualenv`. To start the server and build the local virtual environment run:

   ``make run``
  
It will create a virtual environment with all dependencies locally and use that to start the server.

## API Endpoints

There are two API endpoints, `/train` and `/predict`. `/train` downloads the training dataset and trains all models described below. To train the models run:

   ``curl 127.0.0.1:5000/train``

In order to make a prediction on a new data point we need to post a JSON that represents the observation to `/predict`. For example, the following JSON:

   ```json
      {"age": 75,
      "anaemia": 0,
      "creatinine_phosphokinase": 582,
      "diabetes": 0,
      "ejection_fraction": 20,
      "high_blood_pressure": 1,
      "platelets": 265000,
      "serum_creatinine": 1.9,
      "serum_sodium": 130,
      "sex": 1,
      "smoking": 0,
      "time": 4}
   ```

To post the JSON above run the following command:

   ``curl 127.0.0.1:5000/predict -d '{"age": 75, "anaemia": 0, "creatinine_phosphokinase": 582, "diabetes": 0, "ejection_fraction": 20, "high_blood_pressure": 1, "platelets": 265000, "serum_creatinine": 1.9, "serum_sodium": 130, "sex": 1, "smoking": 0, "time": 4}' -H 'Content-Type: application/json'``

The JSON repsonse gives the predicted class label for each trained model and for the ensemble. For the example above,

```json
{"LR": 1, "GB": 1, "NN": 1, "ensemble": 1}
```

This data point from the training data set is used as an example. 

## Machine Learning Model Architecture

Three machine learning models are implemented with a simple preprocessing pipeline and preset parameters.

* Logistic Regression
* Gradient Boosting Classifier
* Multi-layer Perceptron classifier

The chosen models are typically individually good, quick to train, and are diverse in learning strategy, which should make for a strong ensemble. 

Parameter choices:

* Logistic regression is used with balanced class weighting to account for the slight underrepresentation of heart failure events.
* Gradient Boosting uses up to 100 trees with max depth 4
* The neural network uses an architecture with 4 hidden layers of size [8,8,4,4] as this is a relatively small problem with 12 features.

The ensemble uses a soft voting strategy, meaning it chooses a final prediction based on the sum of predicted probabilities for each model.

During development, the ensemble was evaluated using 5-fold cross-validation and its estimated accuracy on a held-out test set was 76%. The current implementation does not prioritise discovering heart failure above correctly discerning the absence of a fatal event, which may be the desired behaviour.

## Limitations

Future iterations could include more detailed data processing and technical improvements.
* For larger models or datasets, asynchronous training and prediction would be needed.
* In the current implementation, on-off features are not utilised as categoricals. Fields such as "sex", "high_blood_pressure", or "diabetes" are binary, and could be treated as such by some of the included models, however at the moment are not further processed.
* Feature engineering to date is very limited, only implementing standard feature scaling.
* Specifying a different URL to download data from, and target variable for prediction in the train is implemented, but not tested.
* Saving trained model to disc and loading a trained model from local to predict from are not supported.
* Prediction method currently expects a single sample at a time.
