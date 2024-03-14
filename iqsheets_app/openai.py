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

def openai_finetune_data(prompts_to_tune):
    """ Function called in Admin to finetune """
    with open(f'iqsheets_app/static/promptrainer_{datetime.now().strftime("%d-%m-%Y")}.json', 'w', encoding='utf-8') as f:
        json.dump(prompts_to_tune, f, ensure_ascii=False)
    openai_trainer()
    
def openai_trainer():
    # Load the dataset
    with open(f'iqsheets_app/static/promptrainer_{datetime.now().strftime("%d-%m-%Y")}.json', 'r', encoding='utf-8') as f:
        dataset = [json.loads(line) for line in f]
    # Initial dataset stats
    print(dataset)
    print(dataset[0])
    # for message in dataset[0]["messages"]:
    #     print(message)
    
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
