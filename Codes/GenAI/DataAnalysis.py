import time
import papermill as pm
import os

import json


from GenAI.GeminiTool import GeminiAnalyzer, DataValues
from GenAI.datavyu import VyuEngine

class DataAnalysis:

    def __init__(self, job): #Getting job object here 
        self.job = job
        #self.dv = DataValues(job)
        #self.geminitool = GeminiAnalyzer(self.dv, "../GenAI/Credentials.json")

    def GOIT(self):
        # Path to your IPython Notebook file
        notebook_filename = '../GenAI/gemini_test.ipynb'

        # Parameters to pass into the notebook
        parameters = {
            'param1': self.job.Rows
            # Add more parameters as needed
        }

        print(os.getcwd())

        # Execute the notebook with parameters
        pm.execute_notebook(
            notebook_filename,
            'output_notebook.ipynb',
            parameters=parameters
        )

    def Execute(self):
        job = self.job
        
        #print(job.Title, job.Database, job.Prompt, job.Columns, job.Rows)
        # print("This Jobs is your now")
        # time.sleep(1)
        
        # self.geminitool.CreateDictionary()
        # self.geminitool.SetSafetySetting()
        # self.geminitool.ExtractColumns()
        # self.geminitool.ColumnsToWorkOn()
        # self.geminitool.TemplateCheck()
        # self.geminitool.PreProcess()
        # self.geminitool.CheckProcessSteps()
        # self.geminitool.PerformStep()
        # code = self.geminitool.PerformAnalysis()

        print("RIM")
        ve = VyuEngine(job)
        job = ve.start_engine()
        print("MIR")
        
        # self.GOIT()

        return job
    
