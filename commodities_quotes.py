import investpy as inv
import pandas as pd
import setup
import os

start_date = '1/1/2020'
end_date = '1/1/2021'
quote = 'Gold'


class Quotes:
    def __init__(self,quote,start_date,end_date,time_int='Daily'):
        self.quote=quote
        self.start_date = start_date
        self.end_date= end_date
        self.time_int = time_int

    def get_data(self):
        try:
            data = inv.commodities.get_commodity_historical_data(
                self.quote,
                from_date= self.start_date,
                to_date= self.end_date
                )
            return data
        except RuntimeError:
            print(f'symbol {self.quote} not found')

    def data_to_csv(self,data,path,file_name):
        
        data_path = f'{self.path}/{file_name}.csv'
        print('this is the datapath:', data_path)
        data.to_csv(data_path,index=False)


#info = Quotes(quote,start_date,end_date)
#data = info.get_data()
#print(data)
