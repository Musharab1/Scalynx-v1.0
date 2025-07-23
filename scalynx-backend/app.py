from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai  # Gemini API
import json

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can talk to backend

# 🔑 Set your Gemini API Key
genai.configure(api_key="AIzaSyCoJvgR35gcNMGFWRPgcgnIFBjZf_uWZkY")


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

    # ✨ Updated Prompt: Force PURE JSON (no markdown)
    prompt = f"""
    You are a business analyst. Analyze the following business idea:
    - Idea: "{idea}"
    - Target Market: "{market}"
    - Location: "{location}"

    Provide:
    1. A brief assessment of feasibility.
    2. 2 strengths and 2 weaknesses.
    3. A rating out of 10.
    4. A one-line verdict.

    ⚠️ IMPORTANT: Respond ONLY in valid JSON format.
    Do NOT include markdown or code fences. Do NOT add any extra text.
    JSON Example: {{
        "feasibility": "...",
        "strengths": ["...", "..."],
        "weaknesses": ["...", "..."],
        "rating": "8.5/10",
        "verdict": "..."
    }}
    """

    try:
        # Call Gemini API
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        # Parse response safely
        ai_response = json.loads(response.text.strip())
        return jsonify(ai_response)

    except json.JSONDecodeError:
        return jsonify({"error": "Gemini API returned invalid JSON.", "raw_response": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze-idea', methods=['POST'])
def analyze_idea():
    data = request.get_json()
    idea = data.get('idea')

    if not idea:
        return jsonify({"error": "Please provide the business idea."}), 400

    # ✨ Updated Prompt: Force PURE JSON (no markdown)
    prompt = f"""
    Analyze the business idea: "{idea}".
    Provide:
    - 3 key strengths
    - 3 potential weaknesses
    - Success probability percentage
    - One-line advice for improvement.

    ⚠️ IMPORTANT: Respond ONLY in valid JSON format.
    Do NOT include markdown or code fences. Do NOT add any extra text.
    JSON Example: {{
        "strengths": ["...", "...", "..."],
        "weaknesses": ["...", "...", "..."],
        "success_probability": "80%",
        "advice": "..."
    }}
    """

    try:
        # Call Gemini API
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        # Parse response safely
        ai_response = json.loads(response.text.strip())
        return jsonify(ai_response)

    except json.JSONDecodeError:
        return jsonify({"error": "Gemini API returned invalid JSON.", "raw_response": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
