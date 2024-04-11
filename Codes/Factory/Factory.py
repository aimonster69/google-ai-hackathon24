import threading
import time
import sys

sys.path.insert(0, '../')

from GenAI.DataAnalysis import DataAnalysis

class Job:

    def __init__(self, title):
        self.Title = title
        self.JobID = title
        self.Database = []
        self.Prompt = []
        self.Extension = []
        self.Response = []
        self.Images = []
        self.Codes = []
        self.Executed = False
        self.Status = "Running"

    def GetJobID(self):
        return self.JobID
    
    def GetJobTitle(self):
        return self.Title
    
    def Add(self, databaseuri, prompt):
        self.Database.append(databaseuri)
        self.Prompt.append(prompt)
        
        if ".csv" in databaseuri:
            self.Extension.append(".csv")
        else:
            self.Extension.append(".xls")

    def Run(self, job):
        self.Executed = True
        dataAnalysis = DataAnalysis(job)
        print("SA")
        output = dataAnalysis.Execute()
        self.Response.append(output)
        self.Status = "Completed"
        print("SB")


class Jobs:
    Jobs = []
    ExecutedJobs = []

    def __init__(self):
        print("Init")

    def Add(self, Job):
        if(Job.GetJobID() not in Jobs.Jobs):
            Jobs.Jobs.append(Job)
        else:
            Job.JobID = Job.Title + "_" + str(len(self.Jobs))
            Jobs.Jobs.append(Job)
        
class AnalysisMachine(threading.Thread):
    def __init__(self):
        super().__init__()  # Call the superclass constructor

    def run(self):
        count = 0
        while(True):
            if len(Jobs.Jobs) != 0:
                count = 0
                for job in Jobs.Jobs:
                    job.Run(job)
                    Jobs.Jobs.remove(job)
                    Jobs.ExecutedJobs.append(job)
            else:
                count += 1
            
            if count >= 10:
                break        
            
            time.sleep(3)
            print("Cold Run" + str(count))

        
    

class Factory:
    def __init__(self, privateKeyURL):
        if(privateKeyURL == "ABC"):
            self._access = True


    def Job(self, title):
        return Job(title) if self._access == True else None
    
    def Jobs(self):
        return Jobs() if self._access == True else None
    
    def Analyzer(self):
        return AnalysisMachine() if self._access == True else None
    
    def DataAnalysis(self):
        return DataAnalysis() if self._access == True else None