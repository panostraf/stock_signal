import investpy as inv
import pandas as pd
import setup
import os
import ta
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
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
            self.add_indicators(data)
            

            return data
        except RuntimeError:
            print(f'symbol {self.quote} not found')

    
    def add_indicators(self,data):

        # SMA n =20
        data['ma'] = SMAIndicator(data['Close'],20).sma_indicator()
        data['rsi'] = RSIIndicator(data['Close'],14).rsi()

        return data


class Score:
    def __init__(self,data):
        self.total_score = 0
        self.data = data
        self.signal = 'Neutral'
        try:
            self.ma_price_cross()
        except:
            pass
        try:
            self.trend()
        except:
            pass
        try:
            self.rsi()
        except:
            pass

        self.signal_weight()
        

    def ma_price_cross(self):
        if self.data['Close'][-1] > self.data['ma'][-1] and self.data['Close'][-2] < self.data['ma'][-2]:
            self.total_score += 4
        elif self.data['Close'][-1] < self.data['ma'][-1] and self.data['Close'][-2] > self.data['ma'][-2]:
            self.total_score -= 4
        else:
            pass

    def trend(self):
        if self.data['Close'][-1] > self.data['Close'][-2]:
            self.total_score += 4
        elif self.data['Close'][-1] < self.data['Close'][-2]:
            self.total_score -= 4
        else:
            pass

    def rsi(self):
        # Cross above 30
        if self.data['rsi'][-2] < 30 and self.data['rsi'][-1] > 30:
            self.total_score += 4

        # Cross bellow 70
        elif self.data['rsi'][-2] >70 and self.data['rsi'][-1] < 70:
            self.total_score -= 4

        # Cross above 50
        elif self.data['rsi'][-2] < 50 and self.data['rsi'][-1] > 50:
            self.total_score += 4

        # Cross bellow 50
        elif self.data['rsi'][-2] >50 and self.data['rsi'][-1] < 50:
            self.total_score -= 4

        elif self.data['rsi'][-1] > 50:
            self.total_score += 1
        else:
            pass

    def signal_weight(self):
        if self.total_score > 0:
            if self.total_score > 7:
                self.signal = 'Strong Buy'
            elif self.total_score >= 5:
                self.signal = 'Buy'
            else:
                self.signal = 'Neutral'
        elif self.total_score <0:
            if self.total_score < -7:
                self.signal = 'Strong Sell'
            elif self.total_score <= -5:
                self.signal = 'Sell'
            else:
                self.signal = 'Neutral'
        else:
            self.signal = 'Neutral'


def main():
    start_date = '1/1/2020'
    end_date = '1/1/2021'
    quotes = ['Gold','Crude Oil WTI',
            'US Soybeans','US Cocoa',
            'Orange Juice', 'US Corn']

    datasets = [Quotes(quote,start_date,end_date).data for quote in quotes]
    data = dict(zip(quotes,datasets))

    try:
        os.remove("signal_status.csv")
    except:
        pass
    for key,value in data.items():
        score = Score(value).total_score
        signal = Score(value).signal
        close = value['Close'][-1]
        high = value['High'][-1]
        low = value['Low'][-1]
        open_ = value['Open'][-1]
        volume = value['Volume'][-1]

        
        text = f'{key},{score},{signal},{close},{high},{low},{open_},{volume}\n'
        with open('signal_status.csv','a') as f:
            f.write(text)
        f.close()


if __name__=='__main__':

    main()

    

    
