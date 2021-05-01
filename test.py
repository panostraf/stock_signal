import investpy as inv
import pandas as pd
from tkinter import *
from tkinter import ttk


# commodities_l = inv.get_commodities()
# for item in commodities_l['name']:
#     print(item)


class MainWindow:
	

	def __init__(self,master):
		self.columns = ['Contract','Strength','Signal','Last Check','test1','test2']

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
		self.options = Frame(self.content,width=150)
		self.options.pack(side=LEFT,fill='y')

		self.signals = Frame(self.content)
		self.signals.pack(side=RIGHT,fill=BOTH,expand=1)

		# Create treeview object
		self.signals_tree()

		# Create refresh Button
		self.refresh_btn = Button(self.headers,text='refresh',command=lambda: self.refresh())
		# self.refresh_btn.config(fg='RoyalBlue2')
		self.refresh_btn.pack()
		# Create send me notification button

	def signals_tree(self):
		signals_tree = ttk.Treeview(self.signals)
		signals_tree['columns'] = tuple(self.columns)
		signals_tree.column("#0",minwidth=10)
		signals_tree.heading("#0",text='Label',anchor=CENTER)

		for column in self.columns:
			signals_tree.column(column,anchor=CENTER,width=100)
			signals_tree.heading(column,anchor=CENTER,text=column)

		signals_tree.pack(fill=BOTH,expand=1)

	def add_values(self):
		pass

	def clear_tree(self):
		pass

	def refresh(self):
		

	def notifications(self):
		pass









if __name__=='__main__':
	root = Tk()
	root.geometry("800x800")
	MainWindow(root)
	root.mainloop()