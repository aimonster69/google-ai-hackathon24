import google.generativeai as genai
import pandas as pd
import json
import re

class DataDictionaryGenerator:
    def __init__(self, table_description, gemini_token):
        self.table_description = table_description
        self.gemini_token = gemini_token

        # Fetching credentials
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
            self.gemini_token = creds['gemini_api']

        # Configuring generative AI model
        self.generation_config = {
            "temperature": 0.1,
            "top_p": 1,
            "top_k": 1,
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        genai.configure(api_key=self.gemini_token)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

    def generate_response(self, prompt):
        convo = self.model.start_chat(history=[])
        convo.send_message(prompt)
        return re.sub(r"\*\*([^*]+)\*\*", r"\1", convo.last.text)

    def create_data_dictionary(self, df):
        create_data_dict = f'''Table description: {self.table_description}
        Columns: {df.columns}
        Data (First 5 rows): {df.head()}

        Instruction:
        1. Based on the above mentioned details create a data dictionary/documentation which includes a small description of the table, 
        each column, and the data type of each column.
        2. Be concise and concrete in your response.'''

        data_dict = self.generate_response(create_data_dict)
        return data_dict

# Usage:
table_description = input('Write a description about the data you have uploaded..')
gemini_token = "your_gemini_token_here"
data_dict_generator = DataDictionaryGenerator(table_description, gemini_token)
data_dict = data_dict_generator.create_data_dictionary(your_dataframe)
print(data_dict)