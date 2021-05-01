import investpy as inv
import pandas as pd
import setup
import os
import ta
from ta.trend import SMAIndicator
from ta import add_all_ta_features
import matplotlib.pyplot as plt


class Quotes:
    def __init__(self,quote,start_date,end_date,time_int='Daily'):
        self.quote=quote
        self.start_date = start_date
        self.end_date= end_date
        self.time_int = time_int
        self.data = self.get_data()

    def get_data(self):
        try:
            data = inv.commodities.get_commodity_historical_data(
                self.quote,
                from_date= self.start_date,
                to_date= self.end_date
                )
            add_indicators()

            return data
        except RuntimeError:
            print(f'symbol {self.quote} not found')

    @staticmethod
    def add_indicators():
        clf.data['ma'] = SMAIndicator(data['Close'],20).sma_indicator()


    def data_to_csv(self,data,path,file_name):
        
        data_path = f'{self.path}/{file_name}.csv'
        print('this is the datapath:', data_path)
        data.to_csv(data_path,index=False)

    def simple_plot(self,data):
        plt.figure(1)
        plt.plot(data.index,data['Close'])
        plt.plot(data.index,data['ma'])
        plt.show()


class Signals(Quotes):
    def __init__(self):
        super().__init__(self)
        self.quote=quote
        self.start_date = start_date
        self.end_date= end_date
        self.time_int = time_int
        self.data = data
        self.total_score = 0
        

    def trend_score(self):
        last_value = self.data['Close'][-3:].mean()
        last_ma = self.data['ma'][-3:].mean()
        score = 0
        if last_value > last_ma:
            score += 1
        else:
            score -=1

        self.total_score += score


    def ma_cross(self):
        last_value = self.data['Close'][-1:]
        last_ma = self.data['ma'][-1:]
        last_value_n1 = self.data['Close'][-2:]
        last_ma_n1 = self.data['ma'][-2:]
        score = 0
        if last_value > last_ma and last_ma_n1 < last_ma_n1:
            score += 1
        elif last_value < last_ma and last_ma_n1 > last_ma_n1:
            score -= 1
        else:
            pass

        self.total_score += score

    def total_score(self):
        self.total_score = self.total_score + self.trend_score() + self.ma_cross()
        # self.score


if __name__=='__main__':

    start_date = '1/1/2020'
    end_date = '1/1/2021'
    quotes = ['Gold','Crude Oil WTI','US Corn']

    data = [Quotes(quote,start_date,end_date).data for quote in quotes]

    oed_data = dict(zip(quotes,data))

    print(oed_data['Gold'])

    oed_data['Natural Gas'] = Quotes('Natural Gas',start_date,end_date).data

    print(oed_data.keys())
    # print(oed_data['Crude Oil WTI'].keys())
    # gold = Quotes('Gold',start_date,end_date)
    # oil = Quotes('Crude Oil WTI',start_date,end_date)
    # print('\n\nthis is oil data')
    # print(oil.data)

    # print('\n\n This is gold data:')
    # print(gold.data)

    # print('\n\nthis is oil data')
    # print(oil.data)

    # data = c.get_data()
    # data = c.moving_average(data)
    # print(data)
    # c = Signals()
    # c.total_score()
    

    
