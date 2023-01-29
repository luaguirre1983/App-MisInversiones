#!/usr/bin/env python
# coding: utf-8

# In[35]:


# Importamos las librerías con las que estaré trabajando
import requests
import json
import sqlite3
from datetime import datetime

# Indicamos la función de input para conocer qué stock se quiere solicitar
stock = input("Ingrese ticker a pedir:")
stock_inicio =  input ("Ingrese fecha de inicio (en formato AAAA-mm-dd):")
stock_fin =  input ("Ingrese fecha de fin (en formato AAAA-mm-dd):")
print("Pidiendo datos...")

# Realizamos una solicitud a la API de https://api.polygon.io para obtener los datos de los activos que me interesan actualizar. Para ello armo una lista, que de ser necesario sumar otro stock, lo debería actualizar aquí.
url = f'https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{stock_inicio}/{stock_fin}'
params = {'apiKey': 'yDi5vVBSp38kzp_CwZle07pn_1komWBy'}
response = requests.get(url, params)
data = json.loads(response.text)

# Creamos una conexión con base de datos creada para almacenar historia desde el 01/01/2022
con = sqlite3.connect('MisInversiones.db')

# Creamos el curso para interactuar con los datos
cursor = con.cursor()

# Convertimo el timestamp de la API en un formato de fecha compatible con SQL de manera de poder almacenarlo
from datetime import datetime
for d in data["results"]:
    timestamp = d["t"]
    date_object = datetime.fromtimestamp(timestamp/1000)
    fecha = date_object.strftime('%Y-%m-%d')
    cursor.execute('''
    INSERT INTO Stocks(stock, volumen, precio_promedio, precio_apertura, precio_cierre, precio_maximo, precio_minimo, timestamp, fecha)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',(stock, d['v'], d['vw'], d['o'], d['c'], d['h'], d['l'], d['t'], fecha)
    )
print("Datos guardados correctamente")
# Adicionalmente me pareció más prolijo en esta instancia mostrar los registros insertados, en miras de validar que la consulta y respuesta fueron correctas.
print("Estos fueron los registros ingresados")
# Ejecutamos una consulta SELECT a SQL de los registros ingresados
cursor.execute(f"SELECT * FROM Stocks WHERE stock='{stock}' and fecha>='{stock_inicio}' and fecha<='{stock_fin}'")
# Obtenemos los resultados
resultados = cursor.fetchall()
# Imprimimos los resultados
for resultado in resultados:
    print(resultado)
# Comitimos a la base de datos y cerramos la conexión
con.commit()
con.close()

