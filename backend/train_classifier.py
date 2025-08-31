import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline  # Importar Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from utils_text import preprocess_text

print("Iniciando o treinamento do modelo...")

df = pd.read_csv("../data/examples.csv")

df["clean_text"] = df["text"].apply(preprocess_text)

X = df["clean_text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(max_iter=200, random_state=42))
])

print("Treinando o pipeline...")
pipeline.fit(X_train, y_train)

print("Avaliando o modelo...")
y_pred = pipeline.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de classificação:\n", classification_report(y_test, y_pred))

output_dir = "models"
os.makedirs(output_dir, exist_ok=True)
model_path = os.path.join(output_dir, "email_classifier_pipeline.joblib")
joblib.dump(pipeline, model_path)

print(f"Pipeline completo salvo com sucesso em: {model_path}")