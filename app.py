from flask import Flask, request, send_file, jsonify, render_template, send_from_directory
import os
from TTS.api import TTS
from transformers import pipeline
import whisper
import pytesseract
from PIL import Image
import ast

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load models with error handling
try:
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
    print("TTS model loaded successfully")
except Exception as e:
    print(f"Failed to load TTS model: {e}")

try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    print("Summarizer model loaded successfully")
except Exception as e:
    print(f"Failed to load summarizer model: {e}")

try:
    whisper_model = whisper.load_model("base")
    print("Whisper model loaded successfully")
except Exception as e:
    print(f"Failed to load Whisper model: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except Exception as e:
        print(f"Favicon error: {e}")
        return "", 404

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        text = request.form['text']
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], "output.wav")
        tts.tts_to_file(text=text, file_path=output_file)
        return send_file(output_file, as_attachment=True, download_name="output.wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        text = request.form['text']
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return jsonify({"summary": summary[0]['summary_text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/debug', methods=['POST'])
def debug_code():
    try:
        code = request.form['code']
        ast.parse(code)
        return jsonify({"status": "No syntax errors", "explanation": "Code is syntactically valid."})
    except SyntaxError as e:
        return jsonify({"status": "Error", "explanation": f"Syntax error: {str(e)}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        audio_file = request.files['audio']
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.wav")
        audio_file.save(temp_path)
        result = whisper_model.transcribe(temp_path)
        os.remove(temp_path)
        return jsonify({"transcription": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/handwriting', methods=['POST'])
def recognize_handwriting():
    try:
        image = request.files['image']
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp_image.jpg")
        image.save(temp_path)
        img = Image.open(temp_path)
        text = pytesseract.image_to_string(img)
        os.remove(temp_path)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lipsync', methods=['POST'])
def lipsync():
    try:
        video = request.files['video']
        audio = request.files['audio']
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_video.mp4")
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_audio.wav")
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.mp4")
        
        video.save(video_path)
        audio.save(audio_path)
        
        # Updated os.system call with absolute path
        os.system(f"python wav2lip.py --checkpoint_path \"C:\\Users\\sathi\\OneDrive\\Desktop\\GEN IQ\\models\\wav2lip.pth\" --face \"{video_path}\" --audio \"{audio_path}\" --outfile \"{output_path}\"")
        
        if not os.path.exists(output_path):
            raise Exception("Lip-sync processing failed")
        
        return send_file(output_path, as_attachment=True, download_name="lipsync_output.mp4")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)