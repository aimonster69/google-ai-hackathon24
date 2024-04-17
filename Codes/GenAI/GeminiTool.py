# Importing Dependencies
import google.generativeai as genai
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import re
import os
import traceback
import nltk
from PIL import Image
import time
from itertools import permutations


start = time.time()


class DataValues:
    def __init__(self, job):
        self.job = job
        self.table_description = None
        self.df = None
        self.model = None
        self.datadictresponse = None
        self.gemini_token = None
        self.data_dict = None
        self.safety_setting = None
        self.column_names = None
        self.columns = None
        self.columns_intel = ''
        self.data = None
        self.template_to_choose = None
        self.my_analysis = None
        self.preprocessing_template = None
        self.preprocessing_steps = None
        self.prep_details = None
        self.preprocessing_dict = None
        self.code_transcript = None
        self.table_desription = None
        self.analysis_output = None
        self.model_cv = None



class GeminiAnalyzer:
    def __init__(self, datavalues, credential):
        # Fetching credentials
        self.dv = datavalues
        f = open(credential, 'r')
        creds = json.load(f)
        datavalues.gemini_token = creds['gemini_api']

        #print(datavalues.job.Rows[0])

        data = json.loads(datavalues.job.Rows[0])
        datavalues.df = pd.json_normalize(data)
        datavalues.df.head()

    def generate_response(self, prompt, temperature, safety_setting):
        generation_config = {
        "temperature": temperature,
        "top_p": 1,
        "top_k": 1,
        }
        safety_settings = [
            {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": safety_setting
            },
            {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": safety_setting
            },
            {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": safety_setting
            },
            {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": safety_setting
            },
        ]
        genai.configure(api_key=self.dv.gemini_token)
        self.dv.model = genai.GenerativeModel('gemini-pro')
        self.dv.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)
        convo = self.dv.model.start_chat(history=[])
        convo.send_message(prompt)
        return re.sub(r"\*\*([^*]+)\*\*", r"\1", convo.last.text)
    
    def CreateDictionary(self):
        self.dv.data_dict = {}
        create_data_dict = f'''Table description: {self.dv.table_description}
        Columns: {self.dv.df.columns}
        Data types: {self.dv.df.dtypes}

        Instruction:
        1. Based on the above mentioned details create a data dictionary which a small description of table, each column and the data type of each column.
        2. Don't generate anything else. Be concrete and concise in your response
        3. Give the output in the expected format of a dictionary only!
        '''
        output = '''
        Expected Output -> 
        self.dv.data_dict={
        'tbl_description': 'description of table', 
        'columns': {
                    'Name of the column 1': {'col_description':'description of column 1', 'data_type':'Data Type of the column 1'},
                    'Name of the column 2': {'col_description':'description of column 2', 'data_type':'Data Type of the column 2'},
                    'Name of the column 3': {'col_description':'description of column 3', 'data_type':'Data Type of the column 3'}
                }
        }'''

        create_data_dict+=output

        response = self.generate_response(create_data_dict, 0, 'BLOCK_NONE')
        self.dv.datadictresponse = response
        resp = response.replace("```", "")
        #print(resp)
        exec(resp)

    def SetSafetySetting(self):
        self.dv.safety_setting = 'BLOCK_MEDIUM_AND_ABOVE'
        temperature = 0
        identify_threat_level = f'''

        Role: You are Gemini

        Action: Based on harm categories identify the level of threat as: LOW, MEDIUM or HIGH
        Data: {self.dv.df.head()}
        Harm categories: HARM_CATEGORY_HARASSMENT, HARM_CATEGORY_SEXUALLY_EXPLICIT, HARM_CATEGORY_HATE_SPEECH, HARM_CATEGORY_DANGEROUS_CONTENT

        Instructions:
        1. Restrict your response to only LOW, MEDIUM or HIGH at all costs

        Expected output format: LOW or HIGH etc.'''

        threat_level = self.generate_response(identify_threat_level, temperature, 'BLOCK_NONE')

        if threat_level=='HIGH':
            #print('Taking user consent..')
            self.dv.safety_setting = 'BLOCK_NONE'
        #print('Safety setting has been set to: ', self.dv.safety_setting)

    def ExtractColumns(self):
        self.dv.my_analysis = '''suggest me best possible analysis possible'''
        self.dv.my_analysis += "\nAlways Include: Relevant columns, numbers/figures associated with the analysis."

        identify_colums = f'''Analysis: {self.dv.my_analysis}
        Remember: Almmost every analysis requires some kind of aggregation or grouping.
        First 5 rows of Dataframe for your reference: {self.dv.df.head()}

        Instructions:
        1. Based on the Analysis mentioned, Give the names of the most relevant columns from {self.dv.data_dict} by studying details about each column description.
        2. Don't generate any column(s) of your own
        3. If the analysis request is not direct then identify a logic from the given columns that would help you with the analysis.
        4. Don't write anything else, just the column names.

        Expected Output if relevant columns found:
        Columns: Col 1, Col 2, Col 3 etc.
        '''

        #print("COLUMNS")
        #print(self.dv.data_dict)

        self.dv.column_names = self.generate_response(identify_colums, 0, self.dv.safety_setting)
        #print(self.dv.column_names)


    def ColumnsToWorkOn(self):
        # columns to work on
        # Find the index of "Columns:"
        columns_index = self.dv.column_names.find("Columns:")

        # Extract the text after "Columns:"
        columns_text = self.dv.column_names[columns_index + len("Columns:"):].strip()

        # #print the extracted text
        self.dv.columns = columns_text.split(', ')
        #print(self.dv.columns)

        self.dv.data = self.dv.df[self.dv.columns]
        self.dv.data.head()
        self.dv.columns_intel = ''
        for key, val in self.dv.data_dict['columns'].items():
            if key in self.dv.columns:
                self.dv.columns_intel+=f'{key}: {val}\n'

        #print(self.dv.columns_intel)


    def TemplateCheck(self):
        self.dv.template_check = f'''
        Top 5 rows: {self.dv.data.head()}
        Data: {self.dv.data.columns}

        Based on the above details tell me what type of data is it?
        Rules:
        1. If consists text data then write 'Text'
        2. Else 'Numeric'
        3. Don't write anything else just respond whether it is 'Text' or 'Numeric'
        '''

        self.dv.template_to_choose = self.generate_response(self.dv.template_check, 0, self.dv.safety_setting)
        self.dv.template_to_choose
        #print(self.dv.template_to_choose)


    def drop_high_missing_columns(self, df, missing_threshold=25):
        """Drops columns in a pandas DataFrame that have more than the specified missing value threshold.

        Args:
            df (pd.DataFrame): The DataFrame to process.
            missing_threshold (float, optional): The threshold for the proportion of missing values in a column. Defaults to 0.1 (10%).

        Returns:
            pd.DataFrame: The DataFrame with columns exceeding the missing value threshold dropped.
        """

        # Calculate the percentage of missing values per column
        missing_vals = 100 * df.isnull().sum() / len(df)

        # Identify columns to drop
        cols_to_drop = missing_vals[missing_vals > missing_threshold].index

        # Drop the columns if any
        if len(cols_to_drop) > 0:
            return self.dv.df.drop(cols_to_drop, axis=1)
        else:
            return self.dv.df.copy()  # Return a copy to avoid modifying the original DataFrame

        self.dv.data = drop_high_missing_columns(self.dv.data, missing_threshold=25)
        self.dv.data.head()

    def PreProcess(self):
        # Prompt Template for numeric data - 
        if self.dv.template_to_choose=='Numeric':
            #print("Working")
            self.dv.preprocessing_template = '''
            > Data Imputation:-

                When to use: Data imputation is used to fill in missing values (e.g. Null, None or NaN) in the dataset. Impute mode for categorical and mean/median otherwise.
                For what type of data: This step is applicable to numerical and categorical data.

            > Feature Scaling:-

                When to use: Feature scaling is can be done when the features in the dataset have different scales. 
                Do not scale columns/features that are ordinal in nature like rank, ratings etc at any cost!
                For what type of data: This step is primarily applicable to numerical data, but it can also be used for some types of categorical data.

            > Noise Reduction:-

                When to use: Noise in the data can arise from various sources, such as measurement errors or data collection processes. Noise reduction techniques aim to remove or minimize the impact of noise on the dataset.
                For what type of data: This step is applicable to numerical data, and categorical data.

                Actions:
                For numerical data, apply smoothing techniques such as moving averages or median filters.
                For categorical data, grouping rare categories or merging similar categories can reduce noise.

            > Feature Engineering:-

                When to use: Feature engineering involves creating new features from existing ones or transforming existing features.
                Remember: Do it only when it would help in the analysis.
                For E.g 1 If column like date is involved then make sure the column has a consistent format i.e. "datetime format" - "YYYY-MM-DD" by all means!
                For what type of data: This step is applicable to all types of data.

                Actions:
                Generate new features by combining existing ones, extracting useful information from variables, or creating interaction terms.
                Transform features using mathematical functions such as logarithms, square roots, or polynomial transformations to better capture non-linear relationships.

            > Data Normalization or Standardization:-

                When to use: Normalization or standardization can be applied to scale numerical data to a standard range or distribution if required. 
                You shouldn't do it to columns that are ordinal in nature like rank, rating etc, educational level etc.
                For what type of data: This step is applicable to numerical data

                Actions:
                Scale numerical features to a specific range (e.g., [0, 1]) using min-max scaling or standardize features to have a mean of 0 and standard deviation of 1 using z-score normalization.

            > '''

            pattern = r'> (.*?):-'
            self.dv.preprocessing_steps = re.findall(pattern, self.dv.preprocessing_template)
            self.dv.prep_details = self.dv.preprocessing_template.split('>')[1:-1]

            # #print the extracted text
            #print(self.dv.preprocessing_steps)
            #print(self.dv.prep_details)

        if self.dv.template_to_choose=='Text':
            # Prompt Template for Text data - 
            self.dv.preprocessing_template = '''
            > Data Cleaning:-

                When to use: Should be performed to remove stop words or punctuation marks from text data.
                For what type of data: This step is applicable to textual data.
                
                Actions:
                Remove irrelevant information from text data, such as stop words or punctuation marks.

            > Data Imputation:-

                When to use: Data imputation is used to fill in missing values (e.g. Null, None or NaN) in the dataset. Impute mode for categorical and mean/median otherwise.
                For what type of data: This step is applicable to numerical and categorical data. Text data cleaning techniques can sometimes address missing values, but imputation might be necessary in specific cases.

            > Text Preprocessing:-

                When to use: Text preprocessing involves cleaning and transforming textual data into a format suitable for analysis. 
                Remember you need to do it only when the text is a sentence(s) and not for categorical data. Identify if the data is categorical or not.
                For what type of data: This step is specific to textual data, such as natural language text.

                Actions:
                Lowercase all text
                Apply stemming or lemmatization to reduce words to their root form (if applicable)

            > Noise Reduction:-

                When to use: Noise in the data can arise from various sources, such as measurement errors or data collection processes. Noise reduction techniques aim to remove or minimize the impact of noise on the dataset.
                For what type of data: This step is applicable to numerical data, textual data, and categorical data.

                Actions:
                For numerical data, apply smoothing techniques such as moving averages or median filters.
                For categorical data, grouping rare categories or merging similar categories can reduce noise.

            > Feature Engineering:-

                When to use: Feature engineering involves creating new features from existing ones or transforming existing features to improve the performance of machine learning models. For E.g. If a feature like date is involved and if the data is on a daily basis - aggregate it to weekly or monthly basis for better analysis unless not a stock price data.
                For what type of data: This step is applicable to all types of data.
                Remember: Do it only when it would help in the analysis.
                For E.g 1 If column like date is involved then make sure the column has a consistent format i.e. "datetime format" - "YYYY-MM-DD" by all means!
                For what type of data: This step is applicable to all types of data.

                Actions:
                Generate new features by combining existing ones, extracting useful information from text or categorical variables, or creating interaction terms.
                Transform features using mathematical functions such as logarithms, square roots, or polynomial transformations to better capture non-linear relationships.
                Apply techniques specific to text data, such as TF-IDF (Term Frequency-Inverse Document Frequency) to weight the importance of words.

            > Data Normalization or Standardization:-

                When to use: Normalization or standardization can be applied to scale numerical data to a standard range or distribution if required by the specific model being used. 
                You shouldn't do it to columns that are ordinal in nature like rank, rating etc, educational level etc.
                For what type of data: This step is applicable to numerical data and is optional depending on the model's requirements.

                Actions:
                Scale numerical features to a specific range (e.g., [0, 1]) using min-max scaling or standardize features to have a mean of 0 and standard deviation of 1 using z-score normalization.

            > '''

            pattern = r'> (.*?):-'
            self.dv.preprocessing_steps = re.findall(pattern, self.dv.preprocessing_template)
            self.dv.prep_details = self.dv.preprocessing_template.split('>')[1:-1]

            # #print the extracted text
            #print(self.dv.preprocessing_steps)

    

    def normalize_date_format(self, date_column):
        # Define possible date formats
        # Define the elements (year, month, day)
        elements = ['%Y', '%m', '%d']

        # Generate all permutations
        perms = permutations(elements)

        # Format permutations into strings
        possible_formats = ['/'.join(perm) for perm in perms]

        perms = permutations(elements)
        additional_formats = ['-'.join(perm) for perm in perms]
        possible_formats += additional_formats

        # Initialize an empty list to store normalized dates
        normalized_dates = []

        # Iterate over each date in the date column
        for date_str in date_column:
            # Initialize a variable to store the normalized date
            normalized_date = None
            # Iterate over each possible date format
            for date_format in possible_formats:
                try:
                    # Try to parse the date using the current format
                    normalized_date = pd.to_datetime(date_str, format=date_format).strftime("%Y-%m-%d")
                    # If parsing succeeds, break the loop
                    break
                except ValueError:
                    # If parsing fails, continue to the next format
                    continue
            # If no valid format was found, append None to the list
            if normalized_date is None:
                normalized_dates.append(None)
            else:
                # Otherwise, append the normalized date to the list
                normalized_dates.append(normalized_date)
        
        return normalized_dates

    def SolveDateIssues(self):
        fetch_column = f'''Refer columns info: {self.dv.columns_intel}
        And tell which column refers to date.
        Instructions: Don't generate anything else but the column name.

        Expected output: if present then: Column name - else: '' '''

        date_col = self.generate_response(fetch_column, 0, self.dv.safety_setting)

        if date_col!= '':
            # Assuming df is your DataFrame and 'date_column' is the name of your date column
            self.dv.data[f'{date_col}'] = self.dv.normalize_date_format(self.dv.data[f'{date_col}'])
            self.dv.data[f'{date_col}'] = pd.to_datetime(self.dv.data[f'{date_col}'])
        self.dv.data.head()

    def CheckProcessSteps(self):
        # Checking preprocessing 
        data = self.dv.df
        temperature = 0
        self.dv.preprocessing_dict = {}
        test_of_step = None
        result = False
        #print("BAB", self.dv.preprocessing_steps)
        for idx, step in enumerate(tqdm(self.dv.preprocessing_steps)):
            step_to_take = f'''
            Details -
            Analysis to perform: "{self.dv.my_analysis}"
            Based on the analysis identify if preprocessing "{step}" is required or not
            Columns: {self.dv.columns_intel}
            Data types: {self.dv.data.dtypes}
            Description of data: {self.dv.data.describe()}
            Preprocessing Details: {self.dv.prep_details[idx]}
            Remember: Almost all the type of analysis include aggregation/grouping of data. Based on that identify whether {step} preprocessing step is necessary or not.

            Adhere to below instructions at all costs!
            Instructions -
            0. Consider the details shared above to make the rules for your preprocessing test if needed
            1. Assume the dataframe "data" exists already
            2. Do not read data from anywhere
            3. Write a simple error free code
            4. Write a function that performs the preprocessing test and returns the response of the function in 'True' or 'False'
            5. Write only the code, don't include any other text/explanation in header or footer at any cost.
            6. Install and Import whatever package is necessary
            7. Keep the original dataframe intact. Don't overwrite it - at any cost
            8. If preprocessing step is not applicable for the data mentioned then return 'False'

            Expected Output:
            def preprocessing_test(data):
                # Preprocessing logic

                return True or False based on the logic
            result = preprocessing_test(data)
            '''
            count = 0

            # Automated debugging
            while count<2:
                result = False
                try:
                        if count==0:
                            test_of_step = self.generate_response(step_to_take, temperature, self.dv.safety_setting)
                        test_of_step = test_of_step.replace('python', '')
                        test_of_step = test_of_step.replace('`', '')
                        #print("TOS: ", test_of_step)
                        exec(test_of_step)
                        #print("\nResult", result)
                        self.dv.preprocessing_dict[step] = result
                        break
                    
                except Exception as e:
                    #print(type(data))
                    #print(test_of_step)
                    #print("Error: ", e)
                    
                    error_message = f'''
                    Code:
                    {test_of_step}
                    Traceback of the code: {traceback.format_exc()}

                    Adhere to below instructions at all costs!
                    Instruction:
                    1. Identify the cause of the error and rewrite the code - make it error free
                    2. Don't include any text in your response
                    3. Rewrite the code as a function
                    4. Follow these instructions by all means
                    '''
                    
                    temperature += 0.2
                    test_of_step = self.generate_response(test_of_step, temperature, self.dv.safety_setting)
                    count+=1

        #print(self.dv.preprocessing_dict)

    def PerformStep(self):
        # Performing only those preprocessing steps that are required

        # to know how was preprocessing done - code_transcript
        code_transcript = ''
        temperature = 0
        for key, val in tqdm(self.dv.preprocessing_dict.items()):
            #print("ABC", key, val)
            #print("AAA=>1", key)
            if val==True:
                #print("ABC", key, val)
                #print("AAA=>0", val)
                write_code_for_prep_step = f'''
                Details -
                    Analysis to perform: {self.dv.my_analysis}
                    Preprocessing step: {key}
                    Preprocessing Details: {re.findall(rf'> {key}:-(.*?)>', self.dv.preprocessing_template, re.DOTALL)[0]}
                    Columns: {self.dv.columns_intel}
                    Description of data: {self.dv.data.describe()}
                    Data types of columns: {self.dv.data.dtypes}
                
                Adhere to below instructions at all costs!
                Instructions -
                0. Consider the details shared above for rules of your preprocessing test if required
                1. Assume the dataframe "data" exists already
                2. Do not read or generate data by yourself
                3. Do not mention python language in your response
                4. Write simple code that's easy to understand without any errors
                5. Write a function that performs the preprocessing and return the dataframe after preprocessing it
                6. Only write the code don't include any other text. The code shouldn't have any error be syntactical or logical
                7. Call the function. Make sure you don't return an empty dataframe.
                8. Don't use lambda function to write your code at any cost!
                9. From the function name it should be understandable which preprocessing technique was used.

                Expected output:
                def some_function_name():
                    # Some logic

                    return some_value
                    
                # Calling function
                data = some_function_name()
                '''
                count = 0

                # Automated debugging
                while count<2:
                    try:
                        if count==0:
                            prep_code_output = self.generate_response(write_code_for_prep_step, temperature, self.dv.safety_setting)
                        if count!=0:
                            pass
                        prep_code_output = prep_code_output.replace('`','')
                        exec(prep_code_output)
                        #print("COdE", prep_code_output)
                        break
                    
                    except Exception as e:
                        #print("ERRROROM=>", e)
                        error_message = f'''
                        Code:
                        {write_code_for_prep_step}
                        Traceback of the code: {traceback.format_exc()}

                        Adhere to below instructions at all costs!
                        Instruction:
                        1. Identify the cause of the error and rewrite the code - make it error free
                        2. Don't include any text in your response
                        3. Rewrite the code as a function
                        4. Follow these instructions by all means
                        '''
                        temperature += 0.2
                        write_code_for_prep_step = self.generate_response(write_code_for_prep_step, temperature, self.dv.safety_setting)
                        write_code_for_prep_step = write_code_for_prep_step.replace('python', '')
                        write_code_for_prep_step = write_code_for_prep_step.replace('`', '')
                        count+=1
                        #print("COdE", write_code_for_prep_step)
                
                #print("1--->", prep_code_output)
                self.dv.code_transcript+=prep_code_output+'\n-----------------------------------------\n'
        
        #print("CODE")
        #print(self.dv.code_transcript)


    def PerformAnalysis(self):
        
        # Removing existing files:
        try:
            files = ['viz.png', 'viz.html', 'analysis_result.csv']
            for file in files:
                os.remove(file)
        except:
            pass

        # Perform analysis - 
        #print(self.dv.my_analysis)
        write_code_for_analysis = ''
        count, temperature = 0, 0.2
        while count<2:
            try:
                query = f'''
                Task: {self.dv.my_analysis}
                Remember: Analysis is always some type of aggregation or group of certain columns to get the desired result.

                Instructions:
                1. Write a function in python to execute the task and call the function to execute the code - at all costs
                2. Assume a dataframe with the name "data" already exists.
                3. Dataframe df has the following columns: {self.dv.data.columns}. Use the column names for your refernece while generating the code.
                4. Don't include the code to read the file. Write the code assuming the dataframe already exists.
                5. Don't generate your own data. 
                6. First 5 rows of the dataframe you will work on: {self.dv.data.head(5)}
                7. Dataframe should have {self.dv.data.columns} as its columns only.
                8. Don't write code to train any machine learning model. Write code only to perform the analysis
                9. Save the output of the analysis a csv file: 'analysis_result.csv' at all costs!
                10. Write code only the way shown below.

                Expected output:
                def some_function_name():
                    # Some Logic

                    return some_value

                data = some_function_name()
                '''
                if count==0:
                    write_code_for_analysis = self.generate_response(query, temperature, self.dv.safety_setting)
                write_code_for_analysis = write_code_for_analysis.replace('python', '')
                write_code_for_analysis = write_code_for_analysis.replace('`','')
                exec(write_code_for_analysis)
                break
            except Exception as e:
                error_message = f'''
                    Code:
                    {write_code_for_analysis}
                    Traceback of the code: {traceback.format_exc()}

                    Adhere to below instructions at all costs!
                    Instruction:
                    1. Identify the cause of the error and rewrite the code - make it error free
                    2. Don't include any text in your response
                    3. Rewrite the code as a function
                    4. Follow these instructions by all means
                    '''
                temperature += 0.2
                write_code_for_analysis = self.generate_response(error_message, 0.5, self.dv.safety_setting)
                count+=1
                
            #self.dv.code_transcript += write_code_for_analysis + '\n-----------------------------------------\n'
            print(write_code_for_analysis)
            return write_code_for_analysis


    def InsightTypeIdentification(self):
        # Insight type identification

        analysis_output = open('analysis_result.csv').read()
        insight_prompt = f'''
        Based on the Analysis Output shared below, tell what would be best way to represent the insights of the given analysis - Visualization or Text
        1. Choose Visualization when the number of fields/columns are less but more than one - and thus the chart formed would be readable to user.
        2. Choose Text when the number of values are more or the output length is long.

        Expected Output: Visualization or Text
        Analysis wanted: {self.dv.my_analysis}
        Analysis Output: {analysis_output}
        '''

        insight_choice = self.generate_response(insight_prompt, self.dv.temperature, self.dv.safety_setting)
        insight_choice

    def generate_response_gemini_image(self, prompt, img):
        response = self.dv.model_cv.generate_content([prompt, img], stream=True)
        response.resolve()
        return re.sub(r"\*\*([^*]+)\*\*", r"\1", response.text)

    # To give insights
    def understand_image(self, img):
        prompt = f'''
        Analysis requested: {self.dv.my_analysis}
        Analysis Output: {self.dv.analysis_output}
        Data: {self.dv.data.columns}

        The given image is extracted from the analysis. It is a type of visualisation. 
        If visualization: 
            1. Identify the type of visualization
            2. Using labels and legends extract important and accurate insights with numerical figures or percentages from the visualization if there are any.
            3. The insights should be interesting, accurate and actionable - related to the analysis mentioned.
        
        Instructions:
        1. Make sure above conditions are met.
        2. Do not include anything else in your response. 
        3. Be concise, crisp and concrete. Write insights creatively. Each new insight shouldn't start the same way. Make every insight's beginning look unique.
        4. Refer output analysis to generate actionable insights based on the analysis asked and give business related suggestion if asked.
        '''
        return self.generate_response_gemini_image(prompt, img)
    
    def InsightGeneration(self):
        # Code to generate charts
        if self.dv.insight_choice=='Visualization':
            count, temperature = 0, 0.2
            # vis_code = ''
            while count<2:
                try:
                    visualization_prompt = f'''
                        Information - 
                        Table: {self.dv.table_description}
                        Task: {self.dv.my_analysis}
                        Output: {self.dv.analysis_output}

                        TYPES OF CHARTS:
                        1. Line Chart: Good for trends over time/categories, bad for many data points or complex relationships.
                        2. Bar Chart: Compares categories/frequencies, avoid for many categories or negative values.
                        3. Scatter Plot: Explores relationships between two variables, not ideal for more than 3 variables or unclear patterns.
                        4. Pie Chart: Shows proportions/contribution of a whole, avoid for many categories or unclear comparisons.
                        5. Histogram: Visualizes distribution of continuous data, not for categorical data.
                        6. Box Plot: Compares distributions across categories, avoid if outliers dominate.
                        7. Heatmap: Good for visualizing relationships between many variables, bad for complex data, overwhelming for large datasets
                        8. Word cloud: good for visual exploration of frequent terms in text data, bad for in-depth analysis.
                        9. Network Graph: Shows connections between entities (e.g., social networks, protein interactions), Not ideal for large or dense networks.
                        10. Sankey Diagram: Tracks flows across stages in a process (e.g., customer journeys, material flow). Gets messy with many stages or branches.
                        11. Choropleth Mapbox: Colors geographic regions like country etc based on a data value (e.g., election results, population density). Avoids if data varies greatly within regions.
                        12. Heatmap (Geographic): Colors geographic areas based on data intensity. Overwhelming for cluttered data or small regions.
                        13. Flow Map: Shows movement between geographic locations (e.g., migration patterns, trade routes). Can get confusing with many flows or overlapping paths.

                        DEFAULT CHARTS -:
                        1. Trends over time/categories: Line chart
                        2. Compare categories/frequencies: Bar Chart
                        3. Compare frequency but also has regions like countries involved: Choropleth Mapbox plot - using plotly.graph_objects;
                        4. To show proportions: Pie chart
                        5. Comparing distribution: Box plot
                        6. Visualizing distribution of continous data: Histogram (Geographic) or Choropleth
                        7. Exploration of frequent terms in text data: Word cloud

                        Follow the instructions by all means.
                        Instructions -
                        0. Based on the info available above identify what type of chart would suit the best to convey the insights for "{self.dv.my_analysis}" - consider readability of the chart as well.
                        1. Write code in python to perform an insightful visualization from the output shared to plot it - call the function at costs. Don't write any other text. Just code.
                        2. Make a new dataframe which has the following data: {self.dv.analysis_output} and columns: {self.dv.data.columns} from 'analysis_result.csv'
                        3. Don't generate your own data. Don't equate visualization with "data" variable at any cost.
                        4. Visualization should have title, axis labels, legend etc.
                        5. Save the visualization with the name 'viz.png' and 'viz.html' as well at all costs in the function itself.
                        6. Always show x axis labels with a rotation of 90 degrees if the number of labels are more than 8
                        7. If the chart can be built using Seaborn, Geopandas or Plotly then use it
                        8. Refer Code trascript: {code_transcript} to write an error free code.
                        9. If number of entities/rows representing are more then plot only the first/top 10 rows (and mention it in the graph that you have done it)

                        Expected output:
                        def name_of_visualization(some_parameters):
                            # Some Logic

                            # Code to plot and show the chart
                            
                            # Code to save the chart/figure with name "Viz.png" and "Viz.html"
                        
                        # calling the function by all means
                        name_of_visualization(some_parameters)
                        '''
                    if count==0:
                        vis_code = self.generate_response(visualization_prompt, temperature, self.dv.safety_setting)
                    #print(1)
                    vis_code = vis_code.replace('python', '')
                    vis_code = vis_code.replace('`', '')
                    exec(vis_code)
                    #print('executed')
                    break

                except Exception as e:
                    error_message = f'''
                        Code: {vis_code}
                        Traceback of the code: {traceback.format_exc()}

                        Adhere to below instructions at all costs!
                        Instruction:
                        1. Identify the cause of the error and rewrite the code - make it error free
                        2. Don't include any text in your response
                        3. Rewrite the code as a function
                        4. Follow these instructions by all means
                        '''
                    temperature += 0.2
                    vis_code = self.generate_response(error_message, temperature, self.dv.safety_setting)
                count+=1
            
            code_transcript += vis_code+'\n-----------------------------------------\n'

            self.dv.model_cv = genai.GenerativeModel('gemini-pro-vision')
            all_items = os.listdir()
            if 'viz.png' in all_items:
                img = Image.open('viz.png')
                viz_insight = self.understand_image(img)
                #print(viz_insight)
            else:
                pass


    def Insight(self):
        if self.dv.insight_choice=='Text':
            textual_insight = f'''
                            Action: Read the analysis output of {self.dv.my_analysis} carefully: {self.dv.analysis_output}

                            Instructions:
                            1. Share the results and give concrete and crisp actionable or interesting insights from it - if there are any.
                            2. Tone: Professional
                            3. Talk always in terms of numbers/figures or percentages
                            4. Don't generate data/insights of your own at any cost.'''

            insights = self.generate_response(textual_insight, 0.5, self.dv.safety_setting)
            #print(insights)

        #print('Execution Time: (in mins)',(time.time()-start)/60)