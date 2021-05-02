import investpy as inv
import pandas as pd
from tkinter import *
from tkinter import ttk
import time
import threading
import commodities_quotes
# commodities_l = inv.get_commodities()
# for item in commodities_l['name']:
#     print(item)


class MainWindow:
    

    def __init__(self,master):
        self.columns = ['Contract','Strength','Signal',
                        'Last','High','Low','Open','Volume',
                        'SMA','RSI','MACD','ADX']

        # Main Frame to host all subframes of the window
        self.main_frame = Frame(master)
        self.main_frame.pack(fill = BOTH,expand=1)

        # Headers frame and content frame are subframes of main
        self.headers = Frame(self.main_frame,height=50)
        self.headers.pack(side=TOP,fill='x')

        self.content = Frame(self.main_frame)
        self.content.pack(side=BOTTOM,fill=BOTH,expand=1)

        # On content frame there are 2 subframes
        # one left for buttons and one for the treeview
        self.options = Frame(self.content,width=0)
        self.options.pack(side=LEFT,fill='y')

        self.signals = Frame(self.content)
        self.signals.pack(side=RIGHT,fill=BOTH,expand=1)

        # Create treeview object
        self.tree_ = self.signals_tree()
        self.tree_.pack(fill=BOTH,expand=1,padx=10,pady=10)

        # Plot Area
        self.plots = Frame(self.signals)
        self.plots.pack(fill=BOTH,expand=1,padx=10,pady=10)
        #populate tree
        self.add_values()


        threading.Thread(target = self.notifications).start()


    def signals_tree(self):
        signals_tree = ttk.Treeview(self.signals)
        signals_tree['columns'] = tuple(self.columns)
        signals_tree.column("#0",width=0,stretch=NO)
        signals_tree.heading("#0",text='',anchor=CENTER)

        for column in self.columns:
            signals_tree.column(column,anchor=CENTER,width=100)
            signals_tree.heading(column,anchor=CENTER,text=column)
        return signals_tree
        

    def add_values(self):
        try:
            data = open('signal_status.csv','r').readlines()
        except FileNotFoundError:
            data = open('signal_status.csv','w+').readlines()
        counter = 0
        for line in data:
            line = line.split(',')
            values = tuple(item for item in line)
            self.tree_.insert(parent='',index='end',iid=counter,text='',values=values) 
            counter +=1


    def clear_tree(self):
        for record in self.tree_.get_children():
            self.tree_.delete(record)


    def refresh(self):
        self.clear_tree()
        self.add_values()
        # self.add_values()

    def notifications(self):
        while True:
            commodities_quotes.main()
            self.refresh()
            time.sleep(5)

            









if __name__=='__main__':
    root = Tk()
    root.geometry("800x800")
    MainWindow(root)
    root.mainloop()

