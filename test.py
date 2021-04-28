import investpy as inv
import pandas as pd


commodities_l = inv.get_commodities()
for item in commodities_l['name']:
    print(item)
