import investpy as inv
import pandas as pd
import setup
import os
import ta
from ta.trend import SMAIndicator, MACD
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
        data['macd'] = MACD(data['Close'],26,12,9).macd()
        data['macd_signal'] = MACD(data['Close'],26,12,9).macd()

        return data


class Score:
    def __init__(self,data):
        self.total_score = 0
        self.data = data
        self.signal = 'Neutral'

        # Attributes to set:
        self.strong_buy = 7
        self.buy = 3
        self.sell = -3
        self.strong_sell = -7
        self.max_score = 10
        self.min_score = -10

        # Value of signal points weight
        self.small = 1
        self.medium = 2
        self.high = 3

        # What affectes the price
        functions = [self.ma_price_cross(),
                    self.macd(),
                    self.rsi(),
                    self.trend()]

        for function in functions:
            try:
                function
            except AttributeError:
                pass

        self.signal_weight()
        

    def ma_price_cross(self):
        if self.data['Close'][-1] > self.data['ma'][-1] and self.data['Close'][-2] < self.data['ma'][-2]:
            self.total_score += self.high
        elif self.data['Close'][-1] < self.data['ma'][-1] and self.data['Close'][-2] > self.data['ma'][-2]:
            self.total_score -= self.high
        else:
            pass

    def macd(self):
        # self.data['macd'] = MACD(self.data['close'],26,12,9).macd()
        pass

    def trend(self):
        if self.data['Close'][-1] > self.data['Close'][-2]:
            self.total_score += self.medium
        elif self.data['Close'][-1] < self.data['Close'][-2]:
            self.total_score -= self.medium
        else:
            pass

    def rsi(self):
        # Cross above 30
        if self.data['rsi'][-2] < 30 and self.data['rsi'][-1] > 30:
            self.total_score += self.medium

        # Cross bellow 70
        elif self.data['rsi'][-2] >70 and self.data['rsi'][-1] < 70:
            self.total_score -= self.medium

        # Cross above 50
        elif self.data['rsi'][-2] < 50 and self.data['rsi'][-1] > 50:
            self.total_score += self.medium

        # Cross bellow 50
        elif self.data['rsi'][-2] >50 and self.data['rsi'][-1] < 50:
            self.total_score -= self.medium

        elif self.data['rsi'][-1] > 50:
            self.total_score += self.medium
        else:
            pass

    def signal_weight(self):
        if self.total_score > self.max_score:
            self.total_score = self.max_score
        if self.total_score < self.min_score:
            self.total_score = self.min_score

        if self.total_score >= self.strong_buy:
            self.signal = 'Strong Buy'
        elif self.buy <= self.total_score < self.strong_buy:
            self.signal = 'Buy'
        elif self.sell <= self.total_score < self.buy:
            self.signal = ' Neutral'
        elif self.strong_sell <= self.total_score < self.sell:
            self.signal = 'Sell'
        else:
            self.signal = 'Strong Sell'


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
    
    pd.set_option("display.max_rows", 100, "display.max_columns", None)

    # main()
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
        print(key,score,signal)

    print(data['Gold'])
    plt.plot(data['Gold'].index,data['Gold']['macd'])
    plt.plot(data['Gold'].index,data['Gold']['macd_signal'])
    plt.show()
    

    
