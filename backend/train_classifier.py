import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
from utils_text import preprocess_text

# Carregar dataset
df = pd.read_csv("../data/examples.csv")

# Pré-processar os textos
df["clean_text"] = df["text"].apply(preprocess_text)

# Separar features e labels
X = df["clean_text"]
y = df["label"]

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Vetorização (TF-IDF)
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Modelo (Logistic Regression, simples e eficaz)
clf = LogisticRegression(max_iter=200)
clf.fit(X_train_vec, y_train)

# Avaliação
y_pred = clf.predict(X_test_vec)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de classificação:\n", classification_report(y_test, y_pred))

# Salvar modelo e vetorizador
joblib.dump(clf, "model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")

print("✅ Modelo e vetorizador salvos com sucesso!")
