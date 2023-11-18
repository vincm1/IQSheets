import os
from dotenv import load_dotenv
from openai import OpenAI
from flask_login import current_user

openai_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=openai_key)

def openai_chat(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        user=f"user_{current_user.id}",
        temperature=0,
        max_tokens=1024
    )
    return response
