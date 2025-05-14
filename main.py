from flask import Flask, render_template, request, jsonify
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

    # Retry logic for 503 errors (model loading)
    max_retries = 3
    retry_delay = 5  # seconds
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
    if 'resume' not in request.files:
        return jsonify({'error': 'Please upload a resume file.'}), 400
    
    resume_file = request.files['resume']
    job_desc = request.form.get('job_desc')
    
    if not resume_file or not job_desc:
        return jsonify({'error': 'Please provide both a resume file and job description.'}), 400
    
    # Read the resume file content
    try:
        resume = resume_file.read().decode('utf-8')
    except Exception as e:
        return jsonify({'error': f'Error reading resume file: {str(e)}'}), 400
    
    resume_words = set(resume.lower().split())
    job_words = set(job_desc.lower().split())
    common = resume_words.intersection(job_words)
    score = min(len(common) / len(job_words) * 100, 100)
    
    return jsonify({'score': round(score, 2), 'matches': list(common)})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
