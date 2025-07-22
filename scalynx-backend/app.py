from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can talk to backend

@app.route('/api/validate-idea', methods=['POST'])
def validate_idea():
    data = request.get_json()
    idea = data.get('idea')
    market = data.get('targetMarket')
    location = data.get('location')

    # Dummy validation logic
    if idea and market and location:
        message = f" Your idea '{idea}' targeting '{market}' in '{location}' looks promising!"
    else:
        message = " Please provide complete details."

    return jsonify({"message": message})

@app.route('/api/analyze-idea', methods=['GET'])
def analyze_idea_get():
    return jsonify({"message": "This endpoint only accepts POST requests. Use a REST client."})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "Backend is running 🟢"}), 200

# New API endpoint: /api/analyze-idea
@app.route('/api/analyze-idea', methods=['POST'])
def analyze_idea():
    data = request.get_json()
    idea = data.get('idea')
    # Simulate analysis (send a dummy response)
    analysis = {
        "strengths": [
            "Addresses a growing market trend",
            "Low competition in selected location"
        ],
        "weaknesses": [
            "Requires high initial investment",
            "Dependent on supply chain stability"
        ],
        "rating": "8.5/10",
        "verdict": "This idea has great potential if you can secure funding."
    }
    return jsonify(analysis)

if __name__ == "__main__":
    app.run(debug=True)
