# heartfailure

The package structure is based on <https://github.com/candidtim/cookiecutter-flask-minimal> which is a very simple Python package scaffold for Flask APIs. I used cookiecutter and modified it slightly to fit the application.

## Run API Server

The API server requires Python 3, `make` and the python package `virtualenv`. To start the server and build the virtual environment run:

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

Three machine learning models are implemented with a simple preprocessing pipeline and default parameters set.

* Logistic Regression
* Gradient Boosting Classifier
* Multi-layer Perceptron classifier

