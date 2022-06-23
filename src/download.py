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

#Remove de rows in the dataframe that are empty strings or are NAN in the Revenue column

df = df[df['revenue']!=""]
print(df)

# Fijarse el tipo de dato que tiene el df
print(type(df))

#Insertar los datos en un sqlite3 para eso convertimos el df en una lista de tuplas
registros = df.to_records(index=False)
lista_tuplas = list(registros)
print(lista_tuplas)

#Usar la funcion connect() de sqlite3 para crear la base de datos.

conectar = sqlite3.connect('Datos.db')

con = conectar.cursor()

con.execute(""" CREATE TABLE revenue (Fecha,Revenue) """)


con.executemany('INSERT INTO revenue VALUES(?,?)', lista_tuplas)

conectar.commit()

for fila in con.execute('SELECT * FROM revenue'):
    print(fila)

   

conectar.close()    



