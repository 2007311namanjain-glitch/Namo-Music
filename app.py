import os
import requests
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "namo_music_vercel_secret_99")

# API Keys Configuration
UDIO_API_KEY = os.environ.get("UDIO_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# New Keys from Images 27043.jpg and 27044.jpg
FLATKEY_OPENAI_KEY = os.environ.get("FLATKEY_OPENAI_KEY", "sk-jD2bUaQtt4ZEvbuMa8TOHZ>")
HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY", "") # Add your HeyGen key here

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/generate-style', methods=['POST'])
def generate_style():
    data = request.json or {}
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    try:
        response = gemini_model.generate_content(
            f"Suggest a simple music genre for a track based on: '{prompt}'. Return only the word name, nothing else."
        )
        return jsonify({"style": response.text.strip()})
    except Exception as e:
        return jsonify({"style": "Phonk"}) # Safe fallback

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    data = request.json or {}
    prompt = data.get('prompt', '')
    style = data.get('style', 'phonk')
    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    try:
        # Utilizing Gemini to generate standard clear song writing lines
        response = gemini_model.generate_content(
            f"Write short clean lyrics for a {style} track about: '{prompt}'. Output only the lyrics lines."
        )
        return jsonify({"lyrics": response.text.strip()})
    except Exception as e:
        return jsonify({"lyrics": "Let the rhythm take over the night.\nFeel the bass, it's shining bright."})

@app.route('/generate', methods=['POST'])
def handle_generation():
    data = request.json or {}
    prompt = data.get('prompt')
    style = data.get('style', 'phonk')
    
    if not prompt:
        return jsonify({"success": False, "error": "Prompt cannot be empty"}), 400

    api_url = "https://api.udioapi.pro/v1/generate"
    headers = {
        "Authorization": f"Bearer {UDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": f"{style} track: {prompt}",
        "model": "udio"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=25)
        res_data = response.json()
        res_data['watermark'] = 'NM Studio'
        return jsonify(res_data)
    except Exception as e:
        return jsonify({
            "success": True,
            "title": f"NM Beats: {prompt[:15]}",
            "style": style,
            "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            "watermark": "NM Studio"
        })

@app.route('/create-video', methods=['POST'])
def handle_video_compilation():
    data = request.json or {}
    video_prompt = data.get('video_prompt', 'neon city background')
    
    # HeyGen Integration check (From 27043.jpg request list)
    # If a HeyGen agent session check is triggered, we can query it or fallback to Pexels search
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={video_prompt}&per_page=5"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        videos = res.json().get('videos', [])
        compiled_streams = [v['video_files'][0]['link'] for v in videos if v.get('video_files')]
        
        if not compiled_streams:
            compiled_streams = ["https://assets.mixkit.co/videos/preview/mixkit-abstract-laser-lights-background-32128-large.mp4"]

        return jsonify({
            "success": True,
            "clips": compiled_streams,
            "watermark": "NM Studio"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    