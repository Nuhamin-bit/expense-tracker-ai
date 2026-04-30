from sklearn.ensemble import IsolationForest
import numpy as np


def train_fraud_model(df):

    if df is None or len(df) < 5:
        return None

    X = df[["amount"]].values

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)

    return model


def detect_fraud(model, amount):

    if model is None:
        return 10

    pred = model.predict([[amount]])

    return 85 if pred[0] == -1 else 10