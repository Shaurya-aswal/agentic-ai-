import os
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path

load_dotenv()

groq_api_key = os.getenv("groq_api_key")
quad_api_key = os.getenv("quad_api_key")
quad_cluster = os.getenv("quad_cluster")
if groq_api_key is None:
    raise ValueError("groq_api_key is not set in the environment variables.")
if quad_api_key is None:
    raise ValueError("quad_api_key is not set in the environment variables.")
if quad_cluster is None:
    raise ValueError("quad_cluster is not set in the environment variables.")


client = Groq(api_key = groq_api_key)
model="llama-3.3-70b-versatile"

role = "user"
prompt = "i love you very much please be my girlfriend and marry me"
user = {"role": role, "content": prompt}

system = {"role": "system", "content": "you are my manager"}

messages = [system, user]
response = client.chat.completions.create(model = model, messages = messages)

print(response.choices[0].message.content)
