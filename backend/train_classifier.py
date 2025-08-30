import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
from utils_text import preprocess_text

def load_examples(path='../data/examples.csv'):
    df = pd.read_csv(path)
    return df

def preprocess_series(df):
    df['text_prep'] = df['text'].apply(preprocess_text)
    return df

def train_and_save(path_save='../backend/models/pipeline.joblib'):
    df = load_examples()
    df = preprocess_series(df)
    X = df['text_prep'].values
    y = df['label'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=8000)),
        ('clf', LogisticRegression(max_iter=400))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds))
    os.makedirs(os.path.dirname(path_save), exist_ok=True)
    joblib.dump(pipeline, path_save)
    print("Modelo salvo em", path_save)

if __name__ == "__main__":
    train_and_save()
