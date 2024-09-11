import os

import openai


def load_open_ai_key():
    openai.api_key = os.getenv('OPENAI_API_KEY')
