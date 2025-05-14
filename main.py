<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GEN IQ</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1F2525, #0A1D37);
            color: #ffffff;
            position: relative;
            min-height: 100vh;
            overflow-x: hidden;
        }
        #app {
            position: relative;
            z-index: 1;
        }
        input, textarea, select {
            background-color: rgba(50, 50, 50, 0.9);
            color: #ffffff;
            border: 1px solid #ffffff;
            border-radius: 8px;
            padding: 8px;
            margin: 10px 0;
            width: 90%;
            max-width: 400px;
            box-sizing: border-box;
        }
        button {
            background: linear-gradient(45deg, #0F52BA, #2ECC71);
            color: #ffffff;
            border-radius: 12px;
            border: none;
            box-shadow: 0 0 15px rgba(46, 204, 113, 0.7);
            display: block;
            margin: 10px auto;
            padding: 12px 24px;
            font-size: 1.1rem;
            font-weight: bold;
            width: 90%;
            max-width: 200px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        button:hover {
            transform: scale(1.1);
            box-shadow: 0 0 25px rgba(15, 82, 186, 0.9);
        }
        button:disabled {
            background: linear-gradient(45deg, #666666, #999999);
            box-shadow: none;
            cursor: not-allowed;
        }
        h2, h3 {
            color: #D3D3D3;
            text-align: center;
        }
        .background-particles {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: 0;
        }
        .particle {
            position: absolute;
            background: radial-gradient(circle, rgba(255, 215, 0, 0.8), transparent);
            border-radius: 50%;
            width: 6px;
            height: 6px;
            animation: float 8s infinite ease-in-out;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        }
        @keyframes float {
            0% { transform: translateY(100vh) scale(0.5); opacity: 0.8; }
            50% { opacity: 1; }
            100% { transform: translateY(-20vh) scale(1.2); opacity: 0; }
        }
        .particle:nth-child(1) { left: 5%; animation-duration: 10s; animation-delay: 0s; }
        .particle:nth-child(2) { left: 15%; animation-duration: 12s; animation-delay: 1s; }
        .particle:nth-child(3) { left: 25%; animation-duration: 9s; animation-delay: 2s; }
        .particle:nth-child(4) { left: 35%; animation-duration: 11s; animation-delay: 3s; }
        .particle:nth-child(5) { left: 45%; animation-duration: 13s; animation-delay: 0.5s; }
        .particle:nth-child(6) { left: 55%; animation-duration: 10s; animation-delay: 1.5s; }
        .particle:nth-child(7) { left: 65%; animation-duration: 14s; animation-delay: 2.5s; }
        .particle:nth-child(8) { left: 75%; animation-duration: 8s; animation-delay: 3.5s; }
        .particle:nth-child(9) { left: 85%; animation-duration: 12s; animation-delay: 4s; }
        .particle:nth-child(10) { left: 95%; animation-duration: 11s; animation-delay: 0.2s; }
        .unique-title {
            font-size: 7rem;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(45deg, #FFD700, #C0C0C0, #FFD700);
            background-size: 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px #FFD700, 0 0 30px #C0C0C0;
            margin: 30px 0;
            animation: neon-glow 4s ease-in-out infinite;
        }
        @keyframes neon-glow {
            0% { background-position: 0%; text-shadow: 0 0 20px #FFD700, 0 0 30px #C0C0C0; }
            50% { background-position: 100%; text-shadow: 0 0 30px #FFD700, 0 0 40px #C0C0C0; }
            100% { background-position: 0%; text-shadow: 0 0 20px #FFD700, 0 0 30px #C0C0C0; }
        }
        .tool-card-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            width: 90%;
            max-width: 1300px;
            margin: 30px auto;
            perspective: 1000px;
        }
        .tool-card {
            background: rgba(20, 20, 30, 0.95);
            color: #ffffff;
            padding: 25px;
            border: 2px solid transparent;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.4s, box-shadow 0.4s, border 0.4s;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 0 15px rgba(15, 82, 186, 0.5);
            transform: rotateY(0deg);
        }
        .tool-card:hover {
            transform: rotateY(5deg) translateY(-10px);
            box-shadow: 0 0 30px rgba(46, 204, 113, 0.7);
            border: 2px solid #0F52BA;
        }
        .tool-card h3 {
            margin: 15px 0;
            font-size: 1.7rem;
            color: #D3D3D3;
            text-shadow: 0 0 5px #D3D3D3;
        }
        .tool-card p {
            font-size: 1rem;
            color: #e0e0e0;
            margin-bottom: 25px;
        }
        .tool-card .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .back-button-container {
            margin: 20px 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .tool-section {
            display: none;
            padding: 20px;
            text-align: center;
        }
        #home {
            display: block;
        }
        .error, .success {
            color: #ff0000;
            margin: 10px 0;
        }
        .success {
            color: #00ff00;
        }
        @media (max-width: 600px) {
            .unique-title {
                font-size: 4.5rem;
            }
            .tool-card-container {
                grid-template-columns: 1fr;
            }
            button {
                width: 95%;
            }
        }
    </style>
</head>
<body>
    <div id="app">
        <!-- Homepage -->
        <div id="home" class="section">
            <h1 class="unique-title">GEN IQ</h1>
            <div class="background-particles">
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
                <div class="particle"></div>
            </div>
            <div class="tool-card-container">
                <div class="tool-card">
                    <h3>🖼️ Text-to-Image</h3>
                    <p>Generate stunning visuals from text prompts using AI.</p>
                    <div class="button-container">
                        <button onclick="navigate('text-to-image')">Text-to-Image</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>🎵 Text-to-Audio</h3>
                    <p>Transform text into speech with multilingual support.</p>
                    <div class="button-container">
                        <button onclick="navigate('text-to-audio')">Text-to-Audio</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>📝 Summarization</h3>
                    <p>Condense lengthy texts into concise summaries.</p>
                    <div class="button-container">
                        <button onclick="navigate('summarization')">Summarization</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>💻 Code Debugger</h3>
                    <p>Analyze and fix Python code with ease.</p>
                    <div class="button-container">
                        <button onclick="navigate('code-debugger')">Code Debugger</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>📄 ATS Score Checker</h3>
                    <p>Optimize your resume for job applications.</p>
                    <div class="button-container">
                        <button onclick="navigate('ats-score-checker')">ATS Score Checker</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>✍️ Poem Generator</h3>
                    <p>Create poems from a theme in various styles.</p>
                    <div class="button-container">
                        <button onclick="navigate('poem-generator')">Poem Generator</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>📚 Story Idea Generator</h3>
                    <p>Generate creative story premises for writing.</p>
                    <div class="button-container">
                        <button onclick="navigate('story-idea-generator')">Story Idea Generator</button>
                    </div>
                </div>
                <div class="tool-card">
                    <h3>😂 Meme Generator</h3>
                    <p>Create memes with AI-generated images and text.</p>
                    <div class="button-container">
                        <button onclick="navigate('meme-generator')">Meme Generator</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Text-to-Image Section -->
        <div id="text-to-image" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>Text-to-Image Generation</h2>
            <input type="text" id="tti-prompt" placeholder="Enter a prompt: A futuristic city" value="A futuristic city">
            <button onclick="generateImage()">Generate Image</button>
            <div id="tti-result"></div>
        </div>

        <!-- Text-to-Audio Section -->
        <div id="text-to-audio" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>Text-to-Audio Conversion</h2>
            <textarea id="tta-text" placeholder="Enter text: Hello, this is a test." rows="5">Hello, this is a test.</textarea>
            <select id="tta-lang">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
            </select>
            <button onclick="generateAudio()">Generate Audio</button>
            <div id="tta-result"></div>
        </div>

        <!-- Summarization Section -->
        <div id="summarization" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>AI-Powered Summarization</h2>
            <textarea id="sum-text" placeholder="Paste your text here..." rows="10"></textarea>
            <div id="sum-stats"></div>
            <label>Number of sentences in summary: <input type="number" id="sum-sentences" min="1" max="5" value="2"></label>
            <button onclick="summarizeText()">Summarize</button>
            <div id="sum-result"></div>
        </div>

        <!-- Code Debugger Section -->
        <div id="code-debugger" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>Code Debugger & Explainer</h2>
            <textarea id="code-text" placeholder="def example():\n    print(undefined_variable)" rows="10">def example():\n    print(undefined_variable)</textarea>
            <button onclick="debugCode()">Debug</button>
            <div id="code-result"></div>
        </div>

        <!-- ATS Score Checker Section -->
        <div id="ats-score-checker" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>ATS Score Checker</h2>
            <label>Paste Your Resume:</label>
            <textarea id="ats-resume" placeholder="Paste your resume text here..." rows="10"></textarea>
            <label>Job Description:</label>
            <textarea id="ats-job-desc" placeholder="Enter job description here..." rows="10"></textarea>
            <button onclick="checkATSScore()">Check Score</button>
            <div id="ats-result"></div>
        </div>

        <!-- Poem Generator Section -->
        <div id="poem-generator" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>Poem Generator</h2>
            <input type="text" id="poem-theme" placeholder="Enter a theme: e.g., Nature" value="Nature">
            <select id="poem-type">
                <option value="haiku">Haiku</option>
                <option value="sonnet">Sonnet</option>
                <option value="free">Free Verse</option>
            </select>
            <button onclick="generatePoem()">Generate Poem</button>
            <div id="poem-result"></div>
        </div>

        <!-- Story Idea Generator Section -->
        <div id="story-idea-generator" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>Story Idea Generator</h2>
            <input type="text" id="story-genre" placeholder="Genre: e.g., Fantasy" value="Fantasy">
            <input type="text" id="story-setting" placeholder="Setting: e.g., Enchanted Forest" value="Enchanted Forest">
            <input type="text" id="story-character" placeholder="Character: e.g., Brave Knight" value="Brave Knight">
            <button onclick="generateStoryIdea()">Generate Story Idea</button>
            <div id="story-idea-result"></div>
        </div>

        <!-- Meme Generator Section -->
        <div id="meme-generator" class="tool-section">
            <div class="back-button-container">
                <button onclick="navigate('home')">Back to Tools</button>
            </div>
            <h2>Meme Generator</h2>
            <input type="text" id="meme-top-text" placeholder="Top Text: e.g., When You Realize" value="When You Realize">
            <input type="text" id="meme-bottom-text" placeholder="Bottom Text: e.g., It's Friday" value="It's Friday">
            <input type="text" id="meme-image-prompt" placeholder="Image Prompt: e.g., Happy Cat" value="Happy Cat">
            <button onclick="generateMeme()">Generate Meme</button>
            <div id="meme-result"></div>
        </div>
    </div>

    <script>
        // Navigation between sections
        function navigate(sectionId) {
            document.querySelectorAll('.section, .tool-section').forEach(section => {
                section.style.display = 'none';
            });
            document.getElementById(sectionId).style.display = 'block';
        }

        // Single-click enforcement
        document.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', function() {
                button.disabled = true;
                setTimeout(() => {
                    button.disabled = false;
                }, 1000);
            });
        });

        // Text-to-Image
        async function generateImage() {
            const prompt = document.getElementById('tti-prompt').value;
            const resultDiv = document.getElementById('tti-result');
            if (!prompt || !prompt.trim()) {
                resultDiv.innerHTML = '<p class="error">Please enter a valid prompt.</p>';
                return;
            }
            resultDiv.innerHTML = '<p>Generating...</p>';
            try {
                const response = await fetch('/generate-image', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'prompt': prompt })
                });
                const data = await response.json();
                if (data.image) {
                    resultDiv.innerHTML = `
                        <img src="${data.image}" alt="Generated Image" style="max-width: 100%;">
                        <button onclick="downloadImage('${data.image}')">Download Image</button>
                    `;
                } else {
                    resultDiv.innerHTML = `<p class="error">Failed to generate image: ${data.error}</p>`;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Network error: ${e.message}</p>`;
            }
        }

        async function downloadImage(imageData) {
            try {
                const formData = new FormData();
                formData.append('image_data', imageData);
                const response = await fetch('/download-image', {
                    method: 'POST',
                    body: formData
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'generated_image.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch (e) {
                alert('Failed to download image: ' + e.message);
            }
        }

        // Text-to-Audio
        async function generateAudio() {
            const text = document.getElementById('tta-text').value;
            const lang = document.getElementById('tta-lang').value;
            const resultDiv = document.getElementById('tta-result');
            if (!text || !text.trim()) {
                resultDiv.innerHTML = '<p class="error">Please enter some text.</p>';
                return;
            }
            resultDiv.innerHTML = '<p>Generating...</p>';
            try {
                const response = await fetch('/generate-audio', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'text': text, 'lang': lang })
                });
                const data = await response.json();
                if (data.audio) {
                    resultDiv.innerHTML = `
                        <audio controls>
                            <source src="${data.audio}" type="audio/wav">
                            Your browser does not support the audio element.
                        </audio>
                        <button onclick="downloadAudio('${data.audio}')">Download Audio</button>
                    `;
                } else {
                    resultDiv.innerHTML = `<p class="error">Failed to generate audio: ${data.error}</p>`;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Network error: ${e.message}</p>`;
            }
        }

        async function downloadAudio(audioData) {
            try {
                const formData = new FormData();
                formData.append('audio_data', audioData);
                const response = await fetch('/download-audio', {
                    method: 'POST',
                    body: formData
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'generated_audio.wav';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch (e) {
                alert('Failed to download audio: ' + e.message);
            }
        }

        // Poem Generator
        async function generatePoem() {
            const theme = document.getElementById('poem-theme').value;
            const poemType = document.getElementById('poem-type').value;
            const resultDiv = document.getElementById('poem-result');
            if (!theme || !theme.trim()) {
                resultDiv.innerHTML = '<p class="error">Please enter a valid theme.</p>';
                return;
            }
            resultDiv.innerHTML = '<p>Generating...</p>';
            try {
                const response = await fetch('/generate-poem', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'theme': theme, 'poem_type': poemType })
                });
                const data = await response.json();
                if (data.poem) {
                    resultDiv.innerHTML = `<pre style="text-align: center;">${data.poem}</pre>`;
                } else {
                    resultDiv.innerHTML = `<p class="error">Failed to generate poem: ${data.error}</p>`;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Network error: ${e.message}</p>`;
            }
        }

        // Story Idea Generator
        async function generateStoryIdea() {
            const genre = document.getElementById('story-genre').value;
            const setting = document.getElementById('story-setting').value;
            const character = document.getElementById('story-character').value;
            const resultDiv = document.getElementById('story-idea-result');
            if (!genre || !setting || !character) {
                resultDiv.innerHTML = '<p class="error">Please provide genre, setting, and character.</p>';
                return;
            }
            resultDiv.innerHTML = '<p>Generating...</p>';
            try {
                const response = await fetch('/generate-story-idea', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'genre': genre, 'setting': setting, 'character': character })
                });
                const data = await response.json();
                if (data.story_idea) {
                    resultDiv.innerHTML = `<p>${data.story_idea}</p>`;
                } else {
                    resultDiv.innerHTML = `<p class="error">Failed to generate story idea: ${data.error}</p>`;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Network error: ${e.message}</p>`;
            }
        }

        // Meme Generator
        async function generateMeme() {
            const topText = document.getElementById('meme-top-text').value;
            const bottomText = document.getElementById('meme-bottom-text').value;
            const imagePrompt = document.getElementById('meme-image-prompt').value;
            const resultDiv = document.getElementById('meme-result');
            if (!topText || !bottomText || !imagePrompt) {
                resultDiv.innerHTML = '<p class="error">Please provide top text, bottom text, and image prompt.</p>';
                return;
            }
            resultDiv.innerHTML = '<p>Generating...</p>';
            try {
                const response = await fetch('/generate-meme', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'top_text': topText, 'bottom_text': bottomText, 'image_prompt': imagePrompt })
                });
                const data = await response.json();
                if (data.meme) {
                    resultDiv.innerHTML = `
                        <img src="${data.meme}" alt="Generated Meme" style="max-width: 100%;">
                        <button onclick="downloadMeme('${data.meme}')">Download Meme</button>
                    `;
                } else {
                    resultDiv.innerHTML = `<p class="error">Failed to generate meme: ${data.error}</p>`;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Network error: ${e.message}</p>`;
            }
        }

        async function downloadMeme(memeData) {
            try {
                const formData = new FormData();
                formData.append('meme_data', memeData);
                const response = await fetch('/download-meme', {
                    method: 'POST',
                    body: formData
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'generated_meme.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch (e) {
                alert('Failed to download meme: ' + e.message);
            }
        }

        // Summarization
        async function summarizeText() {
            const text = document.getElementById('sum-text').value;
            const numSentences = document.getElementById('sum-sentences').value;
            const resultDiv = document.getElementById('sum-result');
            const statsDiv = document.getElementById('sum-stats');

            try {
                const response = await fetch('/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'text': text, 'num_sentences': numSentences })
                });
                const data = await response.json();
                if (data.error) {
                    resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
                    statsDiv.innerHTML = `Sentence count: ${data.stats.sentence_count} | Word count: ${data.stats.word_count}`;
                } else {
                    statsDiv.innerHTML = `Sentence count: ${data.stats.sentence_count} | Word count: ${data.stats.word_count}`;
                    resultDiv.innerHTML = '<strong>Summary:</strong><br>' + data.summary.map((s, i) => `${i + 1}. ${s}`).join('<br>');
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Error: ${e.message}</p>`;
            }
        }

        // Code Debugger
        async function debugCode() {
            const code = document.getElementById('code-text').value;
            const resultDiv = document.getElementById('code-result');

            try {
                const response = await fetch('/debug-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'code': code })
                });
                const data = await response.json();
                if (data.issues) {
                    resultDiv.innerHTML = '<p>Issues found:</p><ul>' + data.issues.map(issue => `<li>${issue}</li>`).join('') + '</ul>';
                } else {
                    resultDiv.innerHTML = `<p class="success">${data.message}</p>`;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Error: ${e.message}</p>`;
            }
        }

        // ATS Score Checker
        async function checkATSScore() {
            const resume = document.getElementById('ats-resume').value;
            const jobDesc = document.getElementById('ats-job-desc').value;
            const resultDiv = document.getElementById('ats-result');

            if (!resume || !jobDesc) {
                resultDiv.innerHTML = '<p class="error">Please provide both a resume and job description.</p>';
                return;
            }

            try {
                const response = await fetch('/check-ats-score', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ 'resume': resume, 'job_desc': jobDesc })
                });
                const data = await response.json();
                if (data.error) {
                    resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
                } else {
                    resultDiv.innerHTML = `
                        <p>ATS Score: ${data.score}%</p>
                        <p>Matches: ${data.matches.join(', ')}</p>
                        <button onclick="downloadATSResult('${encodeURIComponent(data.result_text)}')">Download Result</button>
                    `;
                }
            } catch (e) {
                resultDiv.innerHTML = `<p class="error">Error: ${e.message}</p>`;
            }
        }

        async function downloadATSResult(resultText) {
            try {
                const formData = new FormData();
                formData.append('result_text', decodeURIComponent(resultText));
                const response = await fetch('/download-ats-result', {
                    method: 'POST',
                    body: formData
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'ats_score_result.txt';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            } catch (e) {
                alert('Failed to download result: ' + e.message);
            }
        }
    </script>
</body>
</html>
