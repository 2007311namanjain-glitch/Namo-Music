import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.secret_key = "namo_music_vercel_secret_99"

# Core Authorized Developer Token Matrix
UDIO_API_KEY = "sk-947eb41576a148be940ce1fd3353db4b"

@app.route('/generate', methods=['POST'])
def handle_generation():
    data = request.json or {}
    prompt = data.get('prompt')
    style = data.get('style', 'phonk')
    model = data.get('model', 'auto')
    
    if not prompt:
        return jsonify({"success": False, "error": "Prompt khali nahi ho sakta!"}), 400

    api_url = "https://api.udioapi.pro/v1/generate"
    headers = {
        "Authorization": f"Bearer {UDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"{style} style music: {prompt}",
        "model": model if model != "auto" else "udio"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        res_data = response.json()
        return jsonify(res_data)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    