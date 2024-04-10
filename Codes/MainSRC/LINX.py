import sys
sys.path.insert(0, '../')

from Factory.Factory import Factory
from APIs.Jobs import APIs


class LINX:

    def __init__(self):
        print("Welcome to LINX...")
        self.factory = Factory("ABC")
        self.APIs = APIs()

    def Begin(self):
        analyzer = self.factory.Analyzer()
        analyzer.start()
        self.APIs.RunJobsAdd()



def main():
    linx = LINX()
    linx.Begin()


if __name__ == "__main__":
    main()