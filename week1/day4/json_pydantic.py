import os
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
from pydantic import BaseModel

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

# using pydantic to define a schema for the customer ticket

class Ticket(BaseModel):
    Name : str
    issue : str
    phone_number : int

# defining schema 
schema = Ticket.model_json_schema()

# defining the reposnse format to be json object
response_format = {
    "type" : "json_object"
}


# system prompt
system_prompt = f""" this is customer ticket ,extract the info and the schema should be {schema}  and values in json format"""

text = "hello my name is shaurya aswal and i am contacting you because the phone which i purchased from your company is not working properly and i want to return it and get a refund for it ,78381 this is my phone number please contact me as soon as possible"
role = "user"
prompt = f""" this is customer ticket ,extract the personal information {text} """
user = {"role": role, "content": prompt}

system = {"role": "system", "content": system_prompt}

messages = [system, user]
response = client.chat.completions.create(model = model, messages = messages, response_format=response_format)

ans = response.choices[0].message.content


# loading the repsonse
import json
raw_json = json.loads(ans)
ticket = Ticket(**raw_json)
print(ticket.Name)  
print(ticket.issue)