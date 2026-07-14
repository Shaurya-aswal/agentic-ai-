#  libraries imported

from logging import info
import os
from dotenv import load_dotenv
from groq import Groq
import json
from pydantic import BaseModel
from pypdf import PdfReader

# loading the environment variables from .env file
load_dotenv()

groq_api_key = os.getenv("groq_api_key")

if not groq_api_key:
    raise ValueError("groq_api_key is not set in the environment variables.")

# initializing the Groq client with the API key
client = Groq(api_key = groq_api_key)
model  = "llama-3.3-70b-versatile"

# opening the data of the resume from the pdf file
pdf_path = "/Users/apple/agentic ai/week1/project/utils/resume_.pdf"
raw_data = PdfReader(pdf_path)
input_prompt = raw_data.pages[0].extract_text()

# defining the schema for the resume using pydantic
class Resume(BaseModel):
    Experience : int
    Skills : str

schema = Resume.model_json_schema()

response_format = {
    "type" : "json_object"
}

# defining the system prompt for the model

system_prompt = f""" this is the resume of a person ,get the information from  resume and return it in json format  and the schema should be {schema} and values in json format"""


role = "user"
prompt = f""" this is the resume of the person {input_prompt}"""
user = {"role": role,"content": prompt}

system = {"role": "system","content": system_prompt}
messages = [system, user]
 
# info from the resume
response = client.chat.completions.create(model = model,messages = messages,response_format=response_format)
info = response.choices[0].message.content

## matching the requirements with the resume
class Match(BaseModel):
    eligible : str
    percentage : int

match_schema = Match.model_json_schema()

resp_format = {
    "type" : "json_object"
}

system_prompt_match = f"""the schema for the match is {match_schema} and values in json format ,check if the resume the requirements or not and return yes or no in json format with key eligible and value yes or no and also return the percentage out of 100 of match in json format with key percentage"""
required = {"Experience": 1, "Skills": "python, machine learning, deep learning , genai"}

match_prompt = f""" this is the personal information of the person {info} and these are the requirements for the job {required} """

match_user = {"role": role,"content": match_prompt}
match_system = {"role": "system","content": system_prompt_match}
match_messages = [match_system, match_user]
match_response = client.chat.completions.create(model = model,messages = match_messages,response_format=resp_format)

print(match_response.choices[0].message.content)
