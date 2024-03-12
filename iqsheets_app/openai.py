""" API connection to OpenAI """
import os
from openai import OpenAI
from flask_login import current_user
from flask import current_app
from iqsheets_app.models import Prompt

openai_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=openai_key)


def openai_finetune(prompts_to_tune):
    """ Function called by Dashboad route """
    print(current_app.app_context)


def openai_chat(prompt):
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        user=f"user_{current_user.id}",
        temperature=0,
        max_tokens=800
    )
    return response
