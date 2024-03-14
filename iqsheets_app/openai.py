""" API connection to OpenAI """
import os
import json
from datetime import datetime
from openai import OpenAI
from flask_login import current_user
from flask import current_app
from iqsheets_app.models import Prompt

openai_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=openai_key)


def openai_finetune(prompts_to_tune):
    """ Function called in Admin to finetune """
    print(prompts_to_tune)
    with open(f'iqsheets_app/static/promptrainer_{datetime.now().strftime("%d-%m-%Y")}.json', 'w', encoding='utf-8') as f:
        json.dump(prompts_to_tune, f, ensure_ascii=False, indent=4)
    print('here')
    
    
def openai_chat(prompt):
    """ Function called by Dashboad route """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        user=f"user_{current_user.id}",
        temperature=0,
        max_tokens=800
    )
    return response
