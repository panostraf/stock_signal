import investpy as inv
import pandas as pd
from tkinter import *
from tkinter import ttk
import time
import threading
import commodities_quotes
import matplotlib.pyplot as plt
import json
from PIL import ImageTk, Image
# commodities_l = inv.get_commodities()
# for item in commodities_l['name']:
#     print(item)


class MainWindow:
    

    def __init__(self,master):

        # last_update = 0
        self.columns = ['Contract','Strength','Signal', 'Last','High','Low','Open','Volume']

        # Main Frame to host all subframes of the window
        self.main_frame = Frame(master)
        self.main_frame.pack(fill = BOTH,expand=1)

        # Headers frame and content frame are subframes of main
        self.headers = Frame(self.main_frame,height=100)
        self.headers.pack(side=TOP,fill='x')

        self.headers_label = Label(self.headers,text='Omen Financial Consulting')
        self.headers_label.pack()

        self.last_update = Label(self.headers,text = f'last_update: {time.strftime("%H:%M:%S", time.localtime())}')
        self.last_update.pack(side=LEFT,padx=10)

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
        self.tree_.bind("<Double-1>", self.printer)
        self.tree_.pack(fill=BOTH,expand=1,padx=10,pady=10)

        # Footer
        self.plots = Frame(self.signals,height=100)#, bg='red')
        self.plots.pack(fill= 'x',expand=1,padx=10, pady=10)


        self.settings_btn = Button(self.headers, text = 'Settings', command = self.settings_)
        self.settings_btn.pack(side = LEFT)


        #populate tree
        self.add_values()

        self.master = master


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
            current_time = time.strftime("%H:%M:%S", time.localtime())
            self.last_update.config(text = f'last_update: {current_time}')
            time.sleep(100)

    def printer(self,event):

        item = self.tree_.selection()
        for i in item:
            name = self.tree_.item(i, "values")[0]
        print(name)

        top = Toplevel()
        bg = ImageTk.PhotoImage(file=f"plots/{name.replace(' ','_')}.jpeg")
        label = Label(top,image=bg)
        label.pack(fill=BOTH,expand=1)
        top.mainloop()

    def settings_(self):
        # top_settings = Toplevel()
        # back = Button(top_settings,text = 'back')
        new = Settings_()
        new.top_settings()
        # bg = ImageTk.PhotoImage(file=f"plots/{name.replace(' ','_')}.jpeg")
        # self.plot_canvas.config(image=bg,anchor='nw')



class Settings_():
    def __init__(self):
        self.top1 = Toplevel()
        self.top1.geometry('500x500')
        self.parameters = read_parameters()
        self.top_settings()
        self.top1.mainloop()

    def close_settings(self):
        self.top1.destroy()

    def top_settings(self):


        def parameters_dict():
            # Get values from entries and save to json
            low = e_low.get()
            medium = e_medium.get()
            high = e_high.get()
            parameters = {  'low':low,
                            'medium': medium,
                            'high': high
                            }
            change_parameters(parameters=parameters)
            self.close_settings()




        lbl_score = Label(self.top1,text='Set point for each scenario')
        lbl_score.grid(row=0,column=0)


        options = ['Low','Medium','High']


        low = Label(self.top1,text = 'Low')
        low.grid(row = 5, column = 0, padx = 10, pady = 5)
        e_low = Entry(self.top1)
        e_low.grid(row = 5, column = 1, padx = 10, pady = 5)
        e_low.insert(0,read_parameters()['low'])

        medium = Label(self.top1,text = 'medium')
        medium.grid(row = 6, column = 0, padx = 10, pady = 5)
        e_medium = Entry(self.top1)
        e_medium.grid(row = 6, column = 1, padx = 10, pady = 5)
        e_medium.insert(0,read_parameters()['medium'])

        high = Label(self.top1,text = 'high')
        high.grid(row = 7, column = 0, padx = 10, pady = 5)
        e_high = Entry(self.top1)
        e_high.grid(row = 7, column = 1, padx = 10, pady = 5)
        e_high.insert(0,read_parameters()['high'])
        
        
        # Save Btn
        save_btn = Button(self.top1, text = 'Save', command = lambda: parameters_dict())
        save_btn.grid(row=8,column=1)


        

def change_parameters(parameters):
    j = json.dumps(parameters)
    with open('parameters.json','w') as f:
        f.write(j)
        f.close()


def read_parameters():
    parameters = json.load(open('parameters.json'))
    # print(parameters)
    return parameters



if __name__=='__main__':
    root = Tk()
    root.geometry("800x800")
    MainWindow(root)
    root.mainloop()
