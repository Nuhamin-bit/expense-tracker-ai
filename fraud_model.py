import numpy as np
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.1, random_state=42)

def train_model(data):
    if len(data) < 5:
        return
    X = np.array(data).reshape(-1, 1)
    model.fit(X)

def detect_fraud(amount):
    prediction = model.predict([[amount]])
    return "Fraud Risk" if prediction[0] == -1 else "Normal"