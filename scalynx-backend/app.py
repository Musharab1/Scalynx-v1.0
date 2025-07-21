from flask import Flask, jsonify, request
from flask_cors import CORS  # 👈 Enable CORS for frontend-backend communication

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Scalynx Backend API!"})

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Backend is working!"})

@app.route('/api/validate-idea', methods=['POST'])
def validate_idea():
    data = request.get_json()

    idea = data.get('idea')
    target_market = data.get('targetMarket')
    location = data.get('location')

    # Dummy logic – you can improve this later
    if not idea or not target_market or not location:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    return jsonify({
        "status": "success",
        "message": f"'{idea}' targeting '{target_market}' in '{location}' sounds promising!"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
