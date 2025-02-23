from flask import Flask, request, send_file, jsonify, render_template
import os
from TTS.api import TTS
from transformers import pipeline
import whisper
import pytesseract
from PIL import Image
import ast

app = Flask(__name__)

# Initialize models
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
whisper_model = whisper.load_model("base")

# Ensure uploads folder exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

# 2️⃣ Text-to-Audio Conversion
@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    output_file = os.path.join(UPLOAD_FOLDER, "output.wav")
    tts.tts_to_file(text=text, file_path=output_file)
    return send_file(output_file, as_attachment=True, download_name="output.wav")

# 3️⃣ AI-Powered Summarization Tool
@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return jsonify({"summary": summary[0]['summary_text']})

# 4️⃣ AI-Based Code Debugger & Explainer
@app.route('/debug', methods=['POST'])
def debug_code():
    code = request.form['code']
    try:
        ast.parse(code)
        return jsonify({"status": "No syntax errors", "explanation": "Code is syntactically valid."})
    except SyntaxError as e:
        return jsonify({"status": "Error", "explanation": f"Syntax error: {str(e)}"})

# 5️⃣ AI-Powered Speech-to-Text Transcriber
@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio_file = request.files['audio']
    temp_path = os.path.join(UPLOAD_FOLDER, "temp.wav")
    audio_file.save(temp_path)
    result = whisper_model.transcribe(temp_path)
    os.remove(temp_path)
    return jsonify({"transcription": result["text"]})

# 6️⃣ AI-Based Handwriting Recognition Tool
@app.route('/handwriting', methods=['POST'])
def recognize_handwriting():
    image = request.files['image']
    temp_path = os.path.join(UPLOAD_FOLDER, "temp_image.jpg")
    image.save(temp_path)
    img = Image.open(temp_path)
    text = pytesseract.image_to_string(img)
    os.remove(temp_path)
    return jsonify({"text": text})

# 7️⃣ AI-Based Face Animation (Lip Syncing)
@app.route('/lipsync', methods=['POST'])
def lipsync():
    video = request.files['video']
    audio = request.files['audio']
    video_path = os.path.join(UPLOAD_FOLDER, "input_video.mp4")
    audio_path = os.path.join(UPLOAD_FOLDER, "input_audio.wav")
    output_path = os.path.join(UPLOAD_FOLDER, "output.mp4")
    
    video.save(video_path)
    audio.save(audio_path)
    
    # Assuming Wav2Lip is set up locally
    os.system(f"python wav2lip.py --checkpoint_path models/wav2lip.pth --face {video_path} --audio {audio_path} --outfile {output_path}")
    
    return send_file(output_path, as_attachment=True, download_name="lipsync_output.mp4")

if __name__ == '__main__':
    app.run(debug=True)