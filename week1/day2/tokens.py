import os
from pathlib import Path
from pyexpat.errors import messages
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_spi_key = os.getenv("groq_api_key")
if not groq_spi_key:
    raise ValueError("groq_api_key is not set in the environment variables.")

client = Groq(api_key = groq_spi_key)
model = "llama-3.3-70b-versatile"
role = "user"
prompt1 = "hi"
prompt2 = "what is your name"
prompt3 = "suggest me name for my food delivery company"

prompts = [prompt1, prompt2, prompt3]
for p in prompts:
    messages = {"role": role , "content": p}

    messages = [messages]
    response = client.chat.completions.create(model = model, messages = messages, temperature=2,max_tokens=100)
    usage = response.usage
    print(f"prompt : {p} ---> input_tokens : {usage.prompt_tokens} , output_tokens : {usage.completion_tokens} , total_tokens : {usage.total_tokens} finish reason : {response.choices[0].finish_reason}")





# system = {"role": "system", "content": "you are a product manager who suggest name for the brand"}

# message = [system, user]

# response = client.chat.completions.create(model = model, messages = message, temperature=2)
# print(response.choices[0].message.content)