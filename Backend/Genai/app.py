from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/htmlcssjsgenerate-code', methods=['POST', 'OPTIONS'])
def generate_html_css_js():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        prompt = data.get('prompt', '')
        language = data.get('language', 'html')
        
        print(f"🎯 Generate request - Language: {language}, Prompt: {prompt}")
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Use the correct model name - try gemini-1.5-pro or gemini-1.5-flash
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as model_error:
            print(f"❌ Model error: {model_error}")
            return jsonify({'error': f'Model not available: {model_error}'}), 500
        
        generation_prompt = f"Generate clean, valid {language} code for: {prompt}. Return only the code without explanations."
        
        response = model.generate_content(generation_prompt)
        
        if not response.text:
            return jsonify({'error': 'Empty response from AI'}), 500
            
        print(f"✅ Generated code: {response.text[:100]}...")
        
        return jsonify({'code': response.text})
        
    except Exception as e:
        print(f"❌ Generation error: {str(e)}")
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/htmlcssjsrefactor-code', methods=['POST', 'OPTIONS'])
def refactor_html_css_js():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        code = data.get('code', '')
        language = data.get('language', 'html')
        
        print(f"🔧 Refactor request - Language: {language}")
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        # Use the correct model name
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as model_error:
            print(f"❌ Model error: {model_error}")
            return jsonify({'error': f'Model not available: {model_error}'}), 500
        
        refactor_prompt = f"Refactor and fix this {language} code: {code}. Return only the refactored code without explanations."
        
        response = model.generate_content(refactor_prompt)
        
        if not response.text:
            return jsonify({'error': 'Empty response from AI'}), 500
            
        print(f"✅ Refactored code: {response.text[:100]}...")
        
        return jsonify({'code': response.text})
        
    except Exception as e:
        print(f"❌ Refactoring error: {str(e)}")
        return jsonify({'error': f'Refactoring failed: {str(e)}'}), 500

# Test route to check available models
@app.route('/test-models', methods=['GET'])
def test_models():
    try:
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
        return jsonify({'available_models': available_models})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')