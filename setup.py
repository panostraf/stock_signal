import os
import pandas as pd

class Folders:
    def __init__(self,name):
        self.name = name
        # path name
        self.path = os.path.abspath(__name__).replace(__name__,'')+name+"/"
        # boolean for path existance
        self.commodities = os.path.exists(self.path)
        

    def check_folders(self):
        # Check if folder with input name exists, and create one if False
        if self.commodities == False:
            print(f'Creating folder {self.name}...')
            try:
                os.mkdir(self.path)
            except FileExistsError:
                pass        


if __name__=='__main__':
    instrument_type = 'commodities'
    Folders(instrument_type).check_folders()
