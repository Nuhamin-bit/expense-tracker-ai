import pickle

model = pickle.load(open("model/expense_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

def predict_category(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]