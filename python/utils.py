import pickle
import numpy as np


def get_scaler():
    with open("../jupyter/data/X_scaler.pickle", 'rb') as xscaler:
        X_scaler = pickle.load(xscaler)
    with open("../jupyter/data/y_scaler.pickle", 'rb') as yscaler:
        y_scaler = pickle.load(yscaler)
    return X_scaler, y_scaler


def get_model():
    with open("../jupyter/data/ML_GBoosting_model.pickle", 'rb') as m:
        _model = pickle.load(m)
    return _model


def predict_price(X):
    X = X_scaler.transform(np.array(X).reshape((1, -1)))
    prediction = model.predict(X)
    prediction = y_scaler.inverse_transform(prediction.reshape(1, -1))[0, 0]
    prediction = round(prediction, 2)
    return prediction


X_scaler, y_scaler = get_scaler()
model = get_model()
