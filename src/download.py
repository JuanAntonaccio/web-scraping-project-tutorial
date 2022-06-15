import requests
import pandas as pd 
from bs4 import BeautifulSoup
import sqlite3

url= "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data=requests.get(url).text
#print(html_data)
result= BeautifulSoup(html_data,"html.parser")
#print(result)
tables = result.find_all("table")
#print(tables)
for index,table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        my_index=index

#print(my_index)
df = pd.DataFrame(columns=['date','revenue'])
for row in tables[my_index].tbody.find_all('tr'):
    col = row.find_all('td')
    if col != "":
        fecha = col[0].text
        ingreso = col[1].text.replace("$","").replace(",","")
        df = df.append({"date":fecha, "revenue":ingreso}, ignore_index=True)
        # Probar con una lista

print(df)
