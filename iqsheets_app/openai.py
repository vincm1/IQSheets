import os
from dotenv import load_dotenv
import openai

openai_key = os.getenv('OPENAI_KEY')

openai.api_key = openai_key
model_engine = "text-davinci-003" 

engines = openai.Engine.list()

def openai_chat(prompt):
    completion = openai.Completion.create( 
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.9,
    )

    return completion
