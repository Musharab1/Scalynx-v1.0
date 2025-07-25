from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Add this
import joblib
import re

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# Load vectorizer, selector, model
vectorizer = joblib.load('idea_vectorizer.pkl')
selector = joblib.load('idea_selector.pkl')
model = joblib.load('idea_validator_svm_model.pkl')

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\b\w{1,2}\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/api/validate-idea', methods=['POST'])
def validate_idea():
    data = request.get_json()
    idea = data.get('idea', '')

    cleaned = clean_text(idea)
    tfidf_vec = vectorizer.transform([cleaned])
    selected_vec = selector.transform(tfidf_vec)
    prediction = model.predict(selected_vec)[0]

    return jsonify({
        'idea': idea,
        'valid': bool(prediction),
        'feedback': "Likely Valid" if prediction else "Likely Invalid"
    })

if __name__ == '__main__':
    app.run(debug=True)
