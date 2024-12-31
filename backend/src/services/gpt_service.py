import openai
from config import Config

def analyze_with_gpt(text):
    """
    Analyze text using GPT-4
    """
    print("Starting GPT analysis...")  # Debug log
    print(f"OpenAI API Key exists: {bool(OPENAI_API_KEY)}")  # Debug without exposing key
    
    try:
        openai.api_key = Config.OPENAI_API_KEY
        
        prompt = f"""
        Please analyze the following text and:
        1. Display the content in a clear way, preserving all the information
        2. Perform a comprehensive analysis
        
        Text to analyze:
        {text}
        """
        
        response = openai.ChatCompletion.create(
            model=Config.MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert analyst. Provide clear, structured analysis of documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_CHUNK_SIZE
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Error in GPT analysis: {str(e)}")
