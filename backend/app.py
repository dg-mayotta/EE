from flask import Flask, request, jsonify
from flask_cors import CORS
from docx import Document
import openai
import re
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MAX_CHUNK_SIZE = 4000
MODEL_NAME = "gpt-4"
TEMPERATURE = 0.7

def process_docx(file):
    """
    Process a DOCX file and extract clean text while preserving structure
    """
    try:
        print(f"Starting to process file: {file.filename}")  # Debug log
        doc = Document(file)
        processed_text = []

        print("Processing paragraphs...")  # Debug log
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                # Clean the text while preserving important formatting
                clean_text = re.sub(r'\s+', ' ', paragraph.text)
                clean_text = re.sub(r'[^\w\s.,;:?¿!¡()\-\'\"]+', '', clean_text)
                
                # Add formatting indicators if paragraph has special styling
                if hasattr(paragraph, 'style') and paragraph.style and paragraph.style.name.startswith('Heading'):
                    clean_text = f"## {clean_text}"
                
                processed_text.append(clean_text.strip())

        print("Processing tables...")  # Debug log
        for table in doc.tables:
            processed_text.append("\nTable:")
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells]
                processed_text.append(" | ".join(row_text))

        final_text = "\n\n".join(processed_text)
        print(f"Processed text length: {len(final_text)}")  # Debug log
        return final_text

    except Exception as e:
        print(f"Error in process_docx: {str(e)}")  # Debug log
        print(traceback.format_exc())  # Print full traceback
        raise

def analyze_with_gpt(text):
    """
    Analyze text using GPT-4
    """
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found in environment variables")
            
        openai.api_key = OPENAI_API_KEY
        
        print(f"Sending chunk of length {len(text)} to GPT")  # Debug log
        
        prompt = f"""
        Please analyze the following Spanish text and:
        1. Display the content in English in a clear way, preserving all the information
        2. Perform a comprehensive analysis
        
        Text to analyze:
        {text}
        """
        
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert analyst. Provide clear, structured analysis of documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_CHUNK_SIZE
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error in analyze_with_gpt: {str(e)}")  # Debug log
        print(traceback.format_exc())  # Print full traceback
        raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "openai_key_set": bool(OPENAI_API_KEY)}), 200

@app.route('/analyze', methods=['POST'])
def analyze_document():
    try:
        print("Starting document analysis...")  # Debug log
        
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        print(f"Received file: {file.filename}")  # Debug log
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.docx'):
            return jsonify({"error": "Only DOCX files are supported"}), 400

        # Extract text from DOCX
        try:
            extracted_text = process_docx(file)
            if not extracted_text:
                return jsonify({"error": "Failed to extract text from document"}), 400
            
            print(f"Successfully extracted text, length: {len(extracted_text)}")  # Debug log
        except Exception as e:
            print(f"Error extracting text: {str(e)}")  # Debug log
            return jsonify({"error": f"Error processing document: {str(e)}"}), 500
        
        # Analyze with GPT-4
        try:
            analysis = analyze_with_gpt(extracted_text)
            
            # Combine results
            final_result = {
                "original_text": extracted_text,
                "analysis": analysis
            }
            
            return jsonify(final_result), 200
            
        except Exception as e:
            print(f"Error in GPT analysis: {str(e)}")  # Debug log
            return jsonify({"error": f"Error in analysis: {str(e)}"}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        print(traceback.format_exc())  # Print full traceback
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
