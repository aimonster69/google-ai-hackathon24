from Factory.Factory import Factory


class LINX:

    def __init__(self):
        print("Welcome to LINX...")
        self.factory = Factory()
        self.Jobs = []

    def PushJob(self):
        self.Jobs.append(self.factory.Job("Job1"))

    

    def RunJob(self):
        for job in self.Jobs:
            job.Run()


    def Begin(self):
        job1 = self.factory.Job("Job1")
        job1.Add("", "")



def main():
    linx = LINX()
    linx.Begin()


if __name__ == "__main__":
    main()