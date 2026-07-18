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
pdf_reader = PdfReader(pdf_path)
resume_text = pdf_reader.pages[0].extract_text()

# defining the schema for the resume using pydantic

class Resume(BaseModel):
    Experience : int
    Skills : str

resume_schema = Resume.model_json_schema()

json_response_format = {
    "type" : "json_object"
}

# defining the system prompt for the model

resume_parser_system_prompt = f""" this is the resume of a person ,get the information from  resume and return it in json format  and the schema should be {resume_schema} and values in json format"""


role = "user"
resume_parser_prompt = f""" this is the resume of the person {resume_text}"""
user_message = {"role": role,"content": resume_parser_prompt}

system_message = {"role": "system","content": resume_parser_system_prompt}
resume_parser_messages = [system_message , user_message]
 
# info from the resume
resume_response = client.chat.completions.create(model = model,messages = resume_parser_messages,response_format=json_response_format)
resume_json = resume_response.choices[0].message.content

## matching the requirements with the resume

class Match(BaseModel):
    eligible : str
    percentage : int

job_match_schema = Match.model_json_schema()


job_match_system_prompt= f"""the schema for the match is {job_match_schema} and values in json format ,check if the resume the requirements or not and return yes or no in json format with key eligible and value yes or no and also return the percentage out of 100 of match in json format with key percentage"""
job_requirements = {"Experience": 1, "Skills": "python, machine learning, deep learning , genai"}
job_match_prompt = f""" this is the personal information of the person {resume_json} and these are the requirements for the job {job_requirements} """

match_user_message = {"role": role,"content": job_match_prompt}
match_system_message= {"role": "system","content": job_match_system_prompt}
job_match_messages = [match_system_message ,match_user_message]
job_match_response = client.chat.completions.create(model = model,messages = job_match_messages,response_format=json_response_format )

print(job_match_response.choices[0].message.content)
