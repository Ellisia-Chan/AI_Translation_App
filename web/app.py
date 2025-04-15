from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import translator, language_detector, text_to_speech

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Render main page"""
    languages = translator.get_languages()
    return render_template('index.html', languages=languages)

@app.route('/api/detect', methods=['POST'])
def detect_language():
    """API endpoint to detect language of text"""
    data = request.json
    text = data.get('text', '')
    
    if not text.strip():
        return jsonify({'success': False, 'error': 'Text is empty'})
        
    result = language_detector.detect_language(text)
    
    if result:
        return jsonify({
            'success': True,
            'language': result
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Could not detect language'
        })

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """API endpoint to translate text"""
    data = request.json
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')
    source_lang = data.get('source_lang')
    
    result = translator.translate_text(text, target_lang, source_lang)
    return jsonify(result)

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """API endpoint to convert text to speech and play it"""
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', 'en')
    
    success = text_to_speech.text_to_speech_memory(text, lang)
    
    return jsonify({
        'success': success,
        'error': None if success else 'Failed to generate speech'
    })

@app.route('/api/stop-audio', methods=['POST'])
def stop_audio():
    """API endpoint to stop any currently playing audio"""
    text_to_speech.stop_audio()
    return jsonify({'success': True})

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """API endpoint to get available languages"""
    return jsonify(translator.get_languages())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
