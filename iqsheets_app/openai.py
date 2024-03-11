""" API connection to OpenAI """
import os
from openai import OpenAI
from flask_login import current_user
from iqsheets_app.models import Prompt

openai_key = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=openai_key)

prompts = Prompt.query.all()
print(prompts[0].prompt_type)

# client.files.create(
#   file=open("mydata.jsonl", "rb"),
#   purpose="fine-tune"
# )


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
