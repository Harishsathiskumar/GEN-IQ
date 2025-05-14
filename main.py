from flask import Flask, render_template, request, jsonify, send_file
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from pylint.lint import Run
from pylint.reporters.text import TextReporter
from io import StringIO
import os
import base64
import time
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt_tab')
    nltk.download('stopwords')

# Hugging Face API Key (Set in Render environment variables)
HF_API_KEY = os.getenv("HF_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    prompt = request.form.get('prompt')
    if not prompt or not prompt.strip():
        return jsonify({'error': 'Prompt is empty or invalid.'}), 400
    if not HF_API_KEY:
        return jsonify({'error': 'Hugging Face API key missing.'}), 400

    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    max_retries = 3
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                image_bytes = response.content
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                return jsonify({'image': f'data:image/png;base64,{image_base64}'})
            elif response.status_code == 503:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return jsonify({'error': 'Model is currently loading or unavailable. Please try again later.'}), 503
            else:
                try:
                    error_detail = response.json().get('error', 'Unknown error')
                except ValueError:
                    error_detail = response.text or 'Unknown error'
                return jsonify({'error': f'API error: {response.status_code} - {error_detail}'}), 500
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Network error: {str(e)}'}), 500
    return jsonify({'error': 'Failed to generate image after multiple attempts.'}), 500

@app.route('/download-image', methods=['POST'])
def download_image():
    image_data = request.form.get('image_data')
    if not image_data:
        return jsonify({'error': 'No image data provided.'}), 400
    
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    
    buffer = io.BytesIO(image_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='generated_image.png',
        mimetype='image/png'
    )

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    text = request.form.get('text')
    lang = request.form.get('lang', 'en')
    
    if not text or not text.strip():
        return jsonify({'error': 'Text is empty or invalid.'}), 400
    if not HF_API_KEY:
        return jsonify({'error': 'Hugging Face API key missing.'}), 400
    
    url = "https://api-inference.huggingface.co/models/facebook/tts_transformer-en-ljspeech"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            audio_bytes = response.content
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return jsonify({'audio': f'data:audio/wav;base64,{audio_base64}'})
        else:
            try:
                error_detail = response.json().get('error', 'Unknown error')
            except ValueError:
                error_detail = response.text or 'Unknown error'
            return jsonify({'error': f'API error: {response.status_code} - {error_detail}'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 500

@app.route('/download-audio', methods=['POST'])
def download_audio():
    audio_data = request.form.get('audio_data')
    if not audio_data:
        return jsonify({'error': 'No audio data provided.'}), 400
    
    audio_data = audio_data.split(',')[1]
    audio_bytes = base64.b64decode(audio_data)
    
    buffer = io.BytesIO(audio_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='generated_audio.wav',
        mimetype='audio/wav'
    )

@app.route('/generate-poem', methods=['POST'])
def generate_poem():
    theme = request.form.get('theme')
    poem_type = request.form.get('poem_type', 'haiku')  # Default to haiku
    
    if not theme or not theme.strip():
        return jsonify({'error': 'Theme is empty or invalid.'}), 400
    if not HF_API_KEY:
        return jsonify({'error': 'Hugging Face API key missing.'}), 400
    
    # Use a generative model for poetry
    url = "https://api-inference.huggingface.co/models/distilgpt2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    if poem_type == 'haiku':
        prompt = f"Write a haiku about {theme}. Follow the 5-7-5 syllable structure:\n"
    elif poem_type == 'sonnet':
        prompt = f"Write a short sonnet (14 lines, iambic pentameter) about {theme}:\n"
    else:
        prompt = f"Write a free verse poem about {theme}:\n"
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 100, "temperature": 0.9}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            poem = response.json()[0]["generated_text"].replace(prompt, "").strip()
            return jsonify({'poem': poem})
        else:
            try:
                error_detail = response.json().get('error', 'Unknown error')
            except ValueError:
                error_detail = response.text or 'Unknown error'
            return jsonify({'error': f'API error: {response.status_code} - {error_detail}'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 500

@app.route('/generate-story-idea', methods=['POST'])
def generate_story_idea():
    genre = request.form.get('genre')
    setting = request.form.get('setting')
    character = request.form.get('character')
    
    if not genre or not setting or not character:
        return jsonify({'error': 'Please provide genre, setting, and character.'}), 400
    if not HF_API_KEY:
        return jsonify({'error': 'Hugging Face API key missing.'}), 400
    
    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    prompt = f"Generate a {genre} story idea set in {setting} featuring a {character}:\n"
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 150, "temperature": 0.8}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            story_idea = response.json()[0]["generated_text"].replace(prompt, "").strip()
            return jsonify({'story_idea': story_idea})
        else:
            try:
                error_detail = response.json().get('error', 'Unknown error')
            except ValueError:
                error_detail = response.text or 'Unknown error'
            return jsonify({'error': f'API error: {response.status_code} - {error_detail}'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 500

@app.route('/generate-meme', methods=['POST'])
def generate_meme():
    top_text = request.form.get('top_text')
    bottom_text = request.form.get('bottom_text')
    image_prompt = request.form.get('image_prompt')
    
    if not top_text or not bottom_text or not image_prompt:
        return jsonify({'error': 'Please provide top text, bottom text, and an image prompt.'}), 400
    if not HF_API_KEY:
        return jsonify({'error': 'Hugging Face API key missing.'}), 400
    
    # Step 1: Generate the image
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": image_prompt}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            try:
                error_detail = response.json().get('error', 'Unknown error')
            except ValueError:
                error_detail = response.text or 'Unknown error'
            return jsonify({'error': f'Image API error: {response.status_code} - {error_detail}'}), 500
        
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Step 2: Add text to the image
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calculate text positions
        img_width, img_height = image.size
        top_text_position = (img_width // 2, 20)
        bottom_text_position = (img_width // 2, img_height - 60)
        
        # Add white text with black outline
        for text, position in [(top_text.upper(), top_text_position), (bottom_text.upper(), bottom_text_position)]:
            # Draw black outline
            for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                draw.text((position[0] + offset[0], position[1] + offset[1]), text, font=font, fill='black', anchor='mm')
            # Draw white text
            draw.text(position, text, font=font, fill='white', anchor='mm')
        
        # Step 3: Convert the image back to base64
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        meme_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return jsonify({'meme': f'data:image/png;base64,{meme_base64}'})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error generating meme: {str(e)}'}), 500

@app.route('/download-meme', methods=['POST'])
def download_meme():
    meme_data = request.form.get('meme_data')
    if not meme_data:
        return jsonify({'error': 'No meme data provided.'}), 400
    
    meme_data = meme_data.split(',')[1]
    meme_bytes = base64.b64decode(meme_data)
    
    buffer = io.BytesIO(meme_bytes)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='generated_meme.png',
        mimetype='image/png'
    )

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form.get('text')
    num_sentences = int(request.form.get('num_sentences', 2))
    
    sentences = sent_tokenize(text)
    words = text.split()
    stats = {'sentence_count': len(sentences), 'word_count': len(words)}
    
    if len(sentences) < 2:
        return jsonify({'error': 'Please enter at least two sentences to summarize.', 'stats': stats}), 400
    if not text.strip():
        return jsonify({'error': 'Please enter some text to summarize.', 'stats': stats}), 400
    
    stop_words = set(stopwords.words("english"))
    words = [w.lower() for w in word_tokenize(text) if w.isalnum() and w.lower() not in stop_words]
    word_freq = Counter(words)
    sentence_scores = {}
    for i, sent in enumerate(sentences):
        score = sum(word_freq[w.lower()] for w in word_tokenize(sent) if w.isalnum() and w.lower() in word_freq)
        sentence_scores[i] = score / (len(word_tokenize(sent)) + 1)
    top_sentences = sorted(sorted(sentence_scores.items(), key=lambda x: x[0])[:num_sentences], key=lambda x: x[1], reverse=True)
    summary = [sentences[i] for i, _ in top_sentences]
    
    return jsonify({'summary': summary, 'stats': stats})

@app.route('/debug-code', methods=['POST'])
def debug_code():
    code = request.form.get('code')
    issues = []
    
    if not code.strip():
        issues.append('Code is empty.')
    if any(len(line) > 120 for line in code.split('\n')):
        issues.append('Some lines exceed 120 characters. Consider breaking them up.')
    
    try:
        with open('temp.py', 'w') as f:
            f.write(code)
        output = StringIO()
        reporter = TextReporter(output)
        Run(['temp.py', '--reports=n'], reporter=reporter, exit=False)
        lint_output = output.getvalue()
        output.close()
        os.remove('temp.py')
        if lint_output.strip():
            issues.extend(lint_output.strip().split('\n'))
        if 'undefined_variable' in code:
            issues.append('Undefined variable: "undefined_variable" is not defined. Define it (e.g., `undefined_variable = \'something\'`) before using it.')
    except Exception as e:
        issues.append(f'Error during linting: {str(e)}')
    
    if not issues:
        return jsonify({'message': 'No issues detected.'})
    return jsonify({'issues': issues})

@app.route('/check-ats-score', methods=['POST'])
def check_ats_score():
    resume = request.form.get('resume')
    job_desc = request.form.get('job_desc')
    
    if not resume or not job_desc:
        return jsonify({'error': 'Please provide both a resume and job description.'}), 400
    
    resume_words = set(resume.lower().split())
    job_words = set(job_desc.lower().split())
    common = resume_words.intersection(job_words)
    score = min(len(common) / len(job_words) * 100, 100)
    
    result_text = f"ATS Score: {round(score, 2)}%\n\nMatched Keywords:\n" + "\n".join(sorted(common))
    
    return jsonify({
        'score': round(score, 2),
        'matches': list(common),
        'result_text': result_text
    })

@app.route('/download-ats-result', methods=['POST'])
def download_ats_result():
    result_text = request.form.get('result_text')
    if not result_text:
        return jsonify({'error': 'No result text provided.'}), 400
    
    buffer = io.BytesIO()
    buffer.write(result_text.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='ats_score_result.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
