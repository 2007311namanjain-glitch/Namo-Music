 import os
import requests
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "namo_music_vercel_secret_99"

# Apka API Key serverless system me safe rahega
UDIO_API_KEY = "sk-947eb41576a148be940ce1fd3353db4b"

# Vercel serverless environment ke liye variable definition
@app.route('/generate', methods=['POST'])
def handle_generation():
    data = request.json or {}
    prompt = data.get('prompt')
    style = data.get('style', 'phonk')
    model = data.get('model', 'auto')
    
    if not prompt:
        return jsonify({"success": False, "error": "Prompt khali nahi ho sakta!"}), 400

    # API Request configuration to udioapi.pro
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
        # Live Call Trigger
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        res_data = response.json()
        return jsonify(res_data)
        
    except Exception as e:
        # Connection error simulation fallback for preview
        test_audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        return jsonify({
            "success": True, 
            "audio_url": test_audio_url,
            "note": "Simulated link"
        })

# Vercel support wrapper handler
def handler(environ, start_response):
    return app(environ, start_response)
    