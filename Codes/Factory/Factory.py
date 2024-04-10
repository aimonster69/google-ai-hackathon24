
class Job:

    def __init(self, title):
        self.Title = title
        self.JobID = title
        self.Database = []
        self.Prompt = []
        self.Extension = []
        self.Response = []
        self.Images = []
        self.Codes = []

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


class Jobs:
    Jobs = []
    ExecutedJobs = []
    def __init__(self):
        print("Jobs")

    def Add(self, Job):
        if(Job.GetJobID() not in self.Jobs):
            Jobs.append(Job)
        else:
            Job.Title = Job.Title + "_" + str(len(self.Jobs))
            Jobs.append(Job)

    def ReadyToExecute
        


class Factory:
    def __init__(self, privateKeyURL):
        if(privateKeyURL == "ABC"):
            self._access = True


    def Job(self, title):
        return Job(title) if self._access == True else None
    
    def Jobs(self):
        return Jobs.Jobs if self._access == True else None