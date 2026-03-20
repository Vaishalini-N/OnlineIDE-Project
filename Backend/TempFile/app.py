from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Add these routes to your existing app.py

@app.route('/htmlcssjsgenerate-code', methods=['POST', 'OPTIONS'])
def generate_code():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.json
        # Add your code generation logic here
        return jsonify({"status": "success", "code": "// Generated code here"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/htmlcssjsrefactor-code', methods=['POST', 'OPTIONS'])
def refactor_code():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.json
        # Add your code refactoring logic here
        return jsonify({"status": "success", "code": "// Refactored code here"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-output', methods=['POST', 'OPTIONS'])
def get_output():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.json
        code = data.get('code', '')
        
        # Execute the code and get output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(['node', temp_file], capture_output=True, text=True, timeout=10)
            output = result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            output = "Execution timeout"
        except Exception as e:
            output = f"Execution error: {str(e)}"
        finally:
            os.unlink(temp_file)
        
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)