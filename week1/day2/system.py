import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_epi_key = os.getenv("groq_api_key")
if not groq_epi_key:
    raise ValueError("groq_api_key is not set in the environment variables.")

client = Groq(api_key = groq_epi_key)
model="llama-3.3-70b-versatile"

role = "user"
prompt = "suggest me name for my food delivery company " 

user = {"role": role, "content": prompt}

system = {"role": "system", "content": "you are a product mangaer who suggest name for the brand "}

message = [system,user]

response = client.chat.completions.create(model = model, messages = message,temperature=2)

print(response.choices[0].message.content)

