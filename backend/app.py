from flask import Flask, request, jsonify
from flask_cors import CORS
from services.docx_service import process_docx
from services.gpt_service import analyze_with_gpt
from utils.text_chunker import chunk_text
import os

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_document():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.docx'):
            return jsonify({"error": "Only DOCX files are supported"}), 400

        # Extract text from DOCX
        extracted_text = process_docx(file)
        if not extracted_text:
            return jsonify({"error": "Failed to extract text from document"}), 400
        
        # Split into chunks if necessary
        text_chunks = chunk_text(extracted_text)
        
        # Analyze with GPT-4
        results = []
        for chunk in text_chunks:
            analysis = analyze_with_gpt(chunk)
            results.append(analysis)
        
        # Combine results
        final_result = {
            "original_text": extracted_text,
            "analysis": results
        }
        
        return jsonify(final_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
