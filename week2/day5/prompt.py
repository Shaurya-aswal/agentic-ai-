import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("groq_api_key")
if not groq_api_key:
    raise ValueError("groq_api_key is not set in the environment variables.")


client = Groq(api_key=groq_api_key)
model = "llama-3.3-70b-versatile"

def llm_ans(prompt):
    message = {
        "role" : "user",
        "content" : prompt
    }
    client = Groq(api_key=groq_api_key)
    model = "llama-3.3-70b-versatile"

    messages = [message]
    response = client.chat.completions.create(model = model, messages = messages)
    ans = response.choices[0].message.content
    return ans

p = """
#ROLE : you are an assistant that works in mobile/laptop company
#task : you have to classify the issue of customer
#constraints : you have to classify the issue of customer in 3 categories: billing, technincal, return
#output_format: you have to ans the issue only in one word in the categories mentioned above
this is customer query:
#fallback : if thereis any query which doesnt match the category ans the query as "other"
my girlfriend broke up with me 
"""
print(llm_ans(p))

