from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.1)

def detect_fraud(df):
    if len(df) < 5:
        df["fraud"] = 0
        return df

    df["fraud"] = model.fit_predict(df[["amount"]])
    df["fraud"] = df["fraud"].apply(lambda x: 1 if x == -1 else 0)
    return df