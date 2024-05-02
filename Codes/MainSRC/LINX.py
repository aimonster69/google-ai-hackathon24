import sys
import webbrowser
import os
import time

sys.path.insert(0, '../')

from Factory.Factory import Factory
from APIs.Jobs import APIs


class LINX:

    isbrowserloaded = False

    def __init__(self):
        print("Welcome to LINX...")
        self.factory = Factory("ABC")
        self.APIs = APIs()

    def RunBrowser(self):
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        #print(f"Parent directory: {parent_dir}")

        filename = parent_dir + "\\FrontEnd\\LINXWeb\\DataVyu.html" 

        try:
            webbrowser.open(filename)
            print("Browser Loaded")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

    def Begin(self):
        self.RunBrowser()
        analyzer = self.factory.Analyzer()
        analyzer.start()
        self.APIs.RunJobsAdd()
        
        



def main():
    linx = LINX()
    linx.Begin()


if __name__ == "__main__":
    main()