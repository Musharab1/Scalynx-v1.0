from flask import Flask, jsonify
from flask_cors import CORS  # 👈 Enable CORS for frontend-backend communication

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to Scalynx Backend API!"})

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Backend is working!"})

if __name__ == '__main__':
    app.run(debug=True)
