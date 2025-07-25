import pandas as pd
import numpy as np
import re
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline

# ===============================
# 1. Load Dataset & Clean Labels
# ===============================
df = pd.read_csv("data/combined_dataset.csv")
print("📊 Original label distribution:\n", df['label'].value_counts())

df['label'] = df['label'].astype(str).str.lower().map({'valid': 1, 'invalid': 0, '1': 1, '0': 0})
df = df[df['label'].isin([0, 1])]
df['label'] = df['label'].astype(int)
print("✅ Cleaned label distribution:\n", df['label'].value_counts())

# ====================
# 2. Text Preprocessing
# ====================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['idea_text'] = df['idea_text'].astype(str).apply(clean_text)

# ================
# 3. Feature Setup
# ================
X = df['idea_text']
y = df['label']

# ================
# 4. TF-IDF Vectorizer
# ================
vectorizer = TfidfVectorizer(
    max_features=15000,
    ngram_range=(1, 2),
    stop_words='english',
    sublinear_tf=True
)
X_vectorized = vectorizer.fit_transform(X)

# Save vectorizer
joblib.dump(vectorizer, 'idea_vectorizer.pkl')

# =========================
# 5. Feature Selection (Chi2)
# =========================
selector = SelectKBest(chi2, k=8000)
X_selected = selector.fit_transform(X_vectorized, y)

# Save selector
joblib.dump(selector, 'idea_selector.pkl')

# =====================
# 6. Train-Test Split
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, stratify=y, random_state=42
)

# =====================
# 7. Train Final Model
# =====================
svm_model = LinearSVC(class_weight='balanced', C=1.0, max_iter=20000)
svm_model.fit(X_train, y_train)

# Save model
joblib.dump(svm_model, 'idea_validator_svm_model.pkl')

# ================
# 8. Evaluation
# ================
svm_preds = svm_model.predict(X_test)
accuracy = accuracy_score(y_test, svm_preds)
print("\n🎯 SVM Accuracy: {:.4f}".format(accuracy))
print(classification_report(y_test, svm_preds))

# ================================
# 9. Cross-Validation with Pipeline
# ================================
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=15000, ngram_range=(1, 2), stop_words='english', sublinear_tf=True)),
    ('clf', LinearSVC(C=1.0, class_weight='balanced', max_iter=10000))
])
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X, y, cv=skf, scoring='accuracy')

print("📈 Stratified CV Scores:", scores)
print("📊 Mean CV Accuracy: {:.2f}%".format(scores.mean() * 100))

# ======================
# 🔮 Sanity Filter Setup
# ======================
def sanity_filter(idea: str) -> bool:
    lower_idea = idea.lower().strip()

    must_have_keywords = [
        # AI/ML/Data
        "ai", "artificial intelligence", "ml", "machine learning", "deep learning",
        "neural network", "data", "big data", "nlp", "natural language processing",
        "computer vision", "image processing", "chatbot", "recommendation system",
        "classification", "regression", "xgboost", "transformer", "llm", "bert", "gpt", "autoencoder",

        # IoT/Hardware
        "iot", "esp32", "esp8266", "stm32", "microcontroller", "sensor", "actuator",
        "smart", "wearable", "embedded", "automation", "raspberry pi", "arduino", "blynk", "mqtt", "zigbee",

        # Healthcare
        "health", "healthcare", "telemedicine", "diagnosis", "disease",
        "patient", "therapy", "mental health", "biomedical", "hospital",
        "covid", "symptom checker", "remote monitoring", "vital signs",

        # Energy & Environment
        "solar", "renewable", "energy", "battery", "power", "green",
        "sustainable", "smart grid", "electric vehicle", "ev", "carbon footprint",
        "inverter", "digital twin", "predictive maintenance", "climate",

        # Education
        "education", "elearning", "learning", "quiz", "students", "teacher",
        "tutor", "course", "learning system", "edtech", "adaptive learning", "assessment", "lms",

        # Finance
        "finance", "fintech", "payment", "transaction", "blockchain",
        "cryptocurrency", "budget", "loan", "investment", "stock", "portfolio", "wallet",

        # Industry
        "automation", "industry", "robot", "predictive maintenance", "smart factory",
        "digital twin", "plc", "scada", "manufacturing", "supply chain", "cobot", "quality control",

        # Social/Environment
        "agriculture", "farming", "crop", "soil", "safety", "accessibility",
        "disaster", "flood", "earthquake", "elderly", "child", "rural", "social impact",
        "waste management", "water purification", "detection", "pollution", "carbon tracking"
    ]

    unrealistic_keywords = [
        "ghost", "alien", "unicorn", "fairy", "dragon", "magic", "wizard", "zombie",
        "vampire", "witch", "teleport", "time travel", "multiverse", "superpower",
        "haunted", "psychic", "chakra", "astrology", "supernatural", "mythical",
        "afterlife", "demon", "curse", "heaven", "hell", "resurrect", "invisible cloak",
        "talking animal", "sorcery", "mind reading", "dream hacking", "flying carpet",
        "ghost detector", "infinity stone", "telekinesis", "horoscope", "immortality",
        "black hole portal", "levitation potion", "shapeshifting", "telepathy helmet"
    ]

    # Reject if any unrealistic term is found
    for bad in unrealistic_keywords:
        if bad in lower_idea:
            print(f"🚫 Rejected (unrealistic): {bad} in \"{idea}\"")
            return False

    # Approve only if at least one realistic keyword is found
    for keyword in must_have_keywords:
        if keyword in lower_idea:
            return True

    print(f"⚠️ Rejected (no relevant tech): \"{idea}\"")
    return False


# ======================
# 🧠 Inference Function
# ======================
import joblib

# Load model components
model = joblib.load('idea_validator_svm_model.pkl')
vectorizer = joblib.load('idea_vectorizer.pkl')
selector = joblib.load('idea_selector.pkl')

# Assume clean_text is defined elsewhere
def predict_idea(texts):
    cleaned = [clean_text(t) for t in texts]
    tfidf_vectors = vectorizer.transform(cleaned)
    selected_features = selector.transform(tfidf_vectors)
    raw_predictions = model.predict(selected_features)

    final_predictions = []
    for i, text in enumerate(texts):
        if not sanity_filter(text):
            final_predictions.append(0)  # Force invalid
        else:
            final_predictions.append(int(raw_predictions[i]))
    return final_predictions


# ======================
# 🧪 Example Usage
# ======================
sample_texts = [
    "AI powered sounded nonesense.",
    "AI system to improve crop prediction using satellite data.",
    "Detect ghost emotions using neural networks and crystal energy.",
    "Blockchain-based smart grid energy optimization.",
    "Flying carpets with GPT-powered recommendation system.",
    "A unicorn-led startup to build chakra-powered teleportation devices."
]

predictions = predict_idea(sample_texts)

for idea, pred in zip(sample_texts, predictions):
    status = "✅ Valid" if pred == 1 else "❌ Invalid"
    print(f"{status} → {idea}")
