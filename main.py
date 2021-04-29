import commodities_quotes as cq
import setup
import os
import time
import pandas as pd


def initial_download(quotes,path,start_date, end_date,
         instrument_type='commodities', ):
    #=os.path.abspath(__name__)):
    for quote in quotes:
        quote_setup = cq.Quotes(quote,start_date,end_date)
        
        data = quote_setup.get_data()
        data = quote_setup.moving_average(data)

        print(path+quote+'.csv')
        data.to_csv(path+quote+'.csv')



if __name__=='__main__':
    
    instrument_type = 'commodities'
    setup_ = setup.Folders(instrument_type)
    setup_.check_folders()
    
    
    path = setup_.path
    print(path)
    
    start_date = '01/01/2010'
    end_date = '01/04/2021'
    quotes = ['Gold','Crude Oil WTI','US Corn']
    initial_download(quotes,path,start_date, end_date,
         instrument_type='commodities')
    
    
