# Importing Dependencies
import google.generativeai as genai
import pandas as pd
import json
import re


def generate_response(prompt):
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", convo.last.text)

def create_data_dictionary(df):
    create_data_dict = f'''Table description: {table_description}
    Columns: {df.columns}
    Data (First 5 columns): {df.head()}

    Instruction:
    1. Based on the above mentioned details create a data dictionary which a small description of table, each column and the data type of each column.
    2. Don't generate anything else. Be concrete and concise in your response.'''

    data_dict = generate_response(create_data_dict)
    return data_dict


# main file
table_description = input('Write a description about the data you have uploaded..')

# Fetching credentials
f = open('credentials.json', 'r')
creds = json.load(f)
gemini_token = creds['gemini_api']

generation_config = {
      "temperature": 0.1,
      "top_p": 1,
      "top_k": 1,
    }
safety_settings = [
    {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]
genai.configure(api_key=gemini_token)
model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

