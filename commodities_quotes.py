import investpy as inv
import pandas as pd
import warnings
import os
import ta
from ta.trend import SMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta import add_all_ta_features
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import gridspec
import multiprocessing
from datetime import datetime
import json
matplotlib.use('TkAgg')


### TODO
### Define weights of scoring
### Add rules more scoring rules
### Create a db to store the results (Replace csv)
### Add options menu on gui
### Add plots of selected field from tree view
### Turn file from commodities only to universal


### URGENT!
### Create initialization file to auto create folders if not exists
### Convert file to .exe

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
            # self.save_data(data)
            # threading.Thread(target = self.save_plots(data)).start()
            

            return data
        except RuntimeError:
            print(f'symbol {self.quote} not found')

    
    def add_indicators(self,data):
        warnings.filterwarnings("ignore",category=RuntimeWarning)
        # SMA n =20
        data['ma'] = SMAIndicator(data['Close'],20).sma_indicator()
        data['rsi'] = RSIIndicator(data['Close'],14).rsi()
        data['macd'] = MACD(data['Close'],26,12,9).macd()
        data['macd_signal'] = MACD(data['Close'],26,12,9).macd_signal()
        data['macd_hist'] = MACD(data['Close'],26,12,9).macd_diff()
        data['adx'] = ADXIndicator(data['High'],data['Low'],data['Close'],14).adx()        
        data['adx_neg'] = ADXIndicator(data['High'],data['Low'],data['Close'],14).adx_neg()
        data['adx_pos'] = ADXIndicator(data['High'],data['Low'],data['Close'],14).adx_pos()

        return data

    def send_signals(self):
        pass




class Score:
    def __init__(self,data):

        self.parameters = json.load(open('parameters.json'))
        
        self.total_score = 0
        self.data = data
        self.signal = 'Neutral'

        # Attributes to set:
        self.strong_buy = 7
        self.buy = 3
        self.sell = -3
        self.strong_sell = -7
        self.max_score = 20
        self.min_score = -20

        # Value of signal points weight
        self.small = int(self.parameters['low'])
        self.medium = int(self.parameters['medium'])
        self.high = int(self.parameters['high'])

        # How many days back to check if condition is met
        self.days_back = 4

        # What affectes the price
        functions = []

        for i in range(self.days_back):
            try:
                # self.ma_price_cross(i),
                self.macd(i),
                self.rsi(i),
                # self.trend()
            except AttributeError:
                pass

        self.signal_weight()
        

    def ma_price_cross(self,i):
        # Check if price crosses above or bellow moving average
        if self.data['Close'][-1+i] > self.data['ma'][-1+i] and self.data['Close'][-2+i] < self.data['ma'][-2+i]:
            self.total_score += self.high
        elif self.data['Close'][-1+i] < self.data['ma'][-1+i] and self.data['Close'][-2+i] > self.data['ma'][-2+i]:
            self.total_score -= self.high
        else:
            pass

    def macd(self,i):
        # Checks if macd crosses macd signal
        if self.data['macd'][-2+i] < self.data['macd_signal'][-2+i] and self.data['macd'][-1+i] > self.data['macd_signal'][-1+i]:
            self.total_score += self.medium
        elif self.data['macd'][-2+i] > self.data['macd_signal'][-2+i] and self.data['macd'][-1+i] < self.data['macd_signal'][-1+i]:
            self.total_score -= self.medium
        pass

    def trend(self):
        # Checks if last day is higher or lower than previous day
        if self.data['Close'][-1] > self.data['Close'][-2]:
            self.total_score += self.small
        elif self.data['Close'][-1] < self.data['Close'][-2]:
            self.total_score -= self.small
        else:
            pass

    def rsi(self,i):
        # Cross above 30
        if self.data['rsi'][-2+i] < 30 and self.data['rsi'][-1+i] > 30:
            self.total_score += self.medium

        # Cross bellow 70
        elif self.data['rsi'][-2+i] >70 and self.data['rsi'][-1+i] < 70:
            self.total_score -= self.medium

        # Cross above 50
        elif self.data['rsi'][-2+i] < 50 and self.data['rsi'][-1+i] > 50:
            self.total_score += self.medium

        # Cross bellow 50
        elif self.data['rsi'][-2+i] >50 and self.data['rsi'][-1+i] < 50:
            self.total_score -= self.medium

        elif self.data['rsi'][-1+i] > 50:
            self.total_score += self.medium
        else:
            pass

    def adx_(self):
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



def save_data(quote,data):
    data.to_csv(f'datasets/{quote}.csv')

def save_plot(quote,data):
    warnings.filterwarnings("ignore",category=UserWarning)
    fig = plt.figure(figsize=(12,8))
    # plt.title(quote)
    charts = gridspec.GridSpec(ncols=1,nrows=4,height_ratios=[4,1,1,1])


    ax1 = fig.add_subplot(charts[0,0])

    # ax1.set_figheight(10)
    ax1.plot(data.index,data['Close'])
    ax1.set_xticks([])
    ax1.set_title(f'{quote} Price')

    ax2 = fig.add_subplot(charts[1,0])
    ax2.plot(data.index,data['macd'])
    ax2.plot(data.index,data['macd_signal'])
    ax2.bar(data.index,data['macd_hist'])
    ax2.set_xticks([])
    ax2.set_title('MACD')


    ax3 = fig.add_subplot(charts[2,0])
    ax3.plot(data.index,data['rsi'])
    ax3.set_xticks([])
    ax3.set_title('RSI')

    ax4 = fig.add_subplot(charts[3,0])
    ax4.plot(data.index,data['adx'])
    ax4.plot(data.index,data['adx_neg'])
    ax4.plot(data.index,data['adx_pos'])
    ax4.set_title('ADX')
    # ax4.set_xticklabels(data.index.astype(datetime),Rotation=45)
    # plt.xticks(Rotation=45)
    # print(data.index)

    plt.savefig(f"plots/{quote.replace(' ','_')}.jpeg", bbox_inches='tight')
   

def main():
    # This function is calling all classes in order to refresh and store data
    # And is called from gui every 2 hours
    start_date = '1/1/2020'
    end_date = '5/5/2021'
    quotes = ['Gold','Crude Oil WTI',
            'US Soybeans','US Cocoa',
            'Orange Juice', 'US Corn']
    # quotes = ['Gold','Orange Juice']
    datasets = [Quotes(quote,start_date,end_date).data for quote in quotes]
    data = dict(zip(quotes,datasets))

    try:
        os.remove("signal_status.csv")
    except:
        pass


    

    for key,value in data.items():

        # Use different proccecor for matplotlib grapghs
        multiprocessing.Process(target=save_plot,args=(key,value[-90:])).start()
        save_data(key,value)

        score = Score(value).total_score
        signal = Score(value).signal
        close = value['Close'][-1]
        high = value['High'][-1]
        low = value['Low'][-1]
        open_ = value['Open'][-1]
        volume = value['Volume'][-1]

        #Save Signals to csv
        text = f'{key},{score},{signal},{close},{high},{low},{open_},{volume}\n'
        with open('signal_status.csv','a') as f:
            f.write(text)
        f.close()


if __name__=='__main__':
    main()

    
