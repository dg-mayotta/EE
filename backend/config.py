import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAX_CHUNK_SIZE = 4000  # Maximum tokens for GPT-4
    MODEL_NAME = "gpt-4"  # or "gpt-4-turbo-preview" if available
    TEMPERATURE = 0.7
