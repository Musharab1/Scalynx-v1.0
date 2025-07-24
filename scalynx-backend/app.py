from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib  # For loading model and vectorizer
import traceback

app = Flask(__name__)
CORS(app)

# ✅ Load ML model and vectorizer
model = joblib.load("model.pkl")        # RandomForestClassifier
vectorizer = joblib.load("vectorizer.pkl")  # TF-IDF or similar

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "✅ Backend is running"}), 200


@app.route('/api/validate-idea', methods=['POST'])
def validate_idea():
    data = request.get_json()
    idea = data.get('idea')
    market = data.get('targetMarket')
    location = data.get('location')

    if not all([idea, market, location]):
        return jsonify({"error": "Please provide complete details."}), 400

    try:
        # Combine all inputs into one string for vectorization
        full_text = f"{idea} {market} {location}"

        # Vectorize using TF-IDF
        features = vectorizer.transform([full_text])

        # Predict probability and label
        probability = model.predict_proba(features)[0][1] * 100  # class "1" = valid
        label = model.predict(features)[0]

        # Make interpretation
        verdict = "Likely to succeed." if label == 1 else "Risky or weak idea."
        rating = f"{round(probability, 1)}/100"

        return jsonify({
            "feasibility": "This is a machine-learned prediction.",
            "strengths": ["Prediction based on past data", "Considers full idea context"],
            "weaknesses": ["No deep reasoning", "Ignores real-time market trends"],
            "rating": rating,
            "verdict": verdict
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze-idea', methods=['POST'])
def analyze_idea():
    data = request.get_json()
    idea = data.get('idea')

    if not idea:
        return jsonify({"error": "Please provide the business idea."}), 400

    try:
        # Vectorize idea only
        features = vectorizer.transform([idea])
        prob = model.predict_proba(features)[0][1] * 100
        label = model.predict(features)[0]

        strengths = ["Model-based decision", "Fast validation", "Data-driven"]
        weaknesses = ["May lack nuance", "Ignores detailed market research", "Can't interpret visuals"]

        advice = "Consider refining your market and competition strategy."
        return jsonify({
            "strengths": strengths,
            "weaknesses": weaknesses,
            "success_probability": f"{round(prob, 1)}%",
            "advice": advice
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
