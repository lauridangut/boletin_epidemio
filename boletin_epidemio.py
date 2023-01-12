#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:53:16 2023

@author: usuario
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import glob
import epiweeks
import datetime
from epiweeks import Week, Year
pd.options.plotting.backend = "plotly"
# import chart_estudio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import plotly.figure_factory as ff
pio.renderers.default='browser'
import seaborn as sns
from pandas.api.types import CategoricalDtype
import dateutil.parser

### Importación de datasets
os.chdir("/home/usuario/Downloads/Laura/PARA_LAU-20220412T150430Z-001/PARA_LAU/2022 CRUDOS-20220614T142637Z-001")
lista_nombres_frames = glob.glob('RESULTADOS *.CSV') # * comodin para buscar
lista_frames = []
for archivo in lista_nombres_frames:
    datos = pd.read_csv(archivo, sep=";", encoding="ISO-8859-1")
    lista_frames.append(datos)
    del(datos)

# Concatenar los dataframes y usar el argumento join porque los archivos están separados por ;
datos = pd.concat(lista_frames, join="outer", ignore_index=True)

# Quedarme con las filas que sí o sí contengan el dato de fecha de muestra
datos = datos[datos['FECHA_REC'].notna()]

### Tratamiento de los datos
# Dar formato de fecha a "FECHA_NACIMIENTO" y "FECHA_REC"
# =============================================================================
# OJOOOOOO!!! LAS FECHAS DE LOS CSV DEBEN TENER EL MISMO FORMATO 
# =============================================================================
def asign_fecha(fecha):
    formatos_fecha = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%m/%d/%y %H:%M", "%m/%d/%Y %H:%M", "%Y/%m/%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y"]
    contador = 0
    while contador < len(formatos_fecha):
        try:
            if bool(datetime.datetime.strptime(fecha, formatos_fecha[contador])) == True:
                fecha_formateada = pd.to_datetime(fecha, format=formatos_fecha[contador]).strftime("%Y/%m/%d")
                return pd.to_datetime(fecha_formateada, format="%Y/%m/%d")
        except ValueError:
            contador += 1
    if contador == len(formatos_fecha):
        print("Error en formato fecha. Cargar archivo CRUDO ", fecha)


for i in range(0, len(datos)):
    datos.FECHA_REC.iloc[i] = asign_fecha(datos.FECHA_REC.iloc[i])

for i in range(0, len(datos)):
    datos.FECHA_NACIMIENTO.iloc[i] = asign_fecha(datos.FECHA_NACIMIENTO.iloc[i])
    
# Agregar columna de semana epidemiológica
for i in range(0, len(datos)):
    fecha = datos["FECHA_REC"].iloc[i]
    datos.at[i,"SEMANA_EPI"] = Week.fromdate(fecha, system="CDC")
    del(fecha, i)

# Agregar columna de edad en meses
datos["EDAD_MESES"] = round((datos["FECHA_REC"] - datos["FECHA_NACIMIENTO"]) / np.timedelta64(1, "M"), 1)
datos.loc[datos.EDAD_MESES<0,'EDAD_MESES']=0

# Agregar columna de edad en años
datos["EDAD_AÑOS"] = round((datos["FECHA_REC"] - datos["FECHA_NACIMIENTO"]) / np.timedelta64(1, "Y"), 1)
datos.loc[datos.EDAD_AÑOS<0,'EDAD_AÑOS']=0

# Agregar columna categoría de edad (list comprehension):
    # 1 < 6 meses
    # 2 = 6 a 11 meses
    # 3 = 11 a 23 meses
    # 4 = 24 a 48 meses
    # 5 = 49 a 108 meses
    # 6 = 109 a 168 meses
    # 7 = 169 a 228 meses
datos["CAT_EDAD"] = [1 if x < 6
                     else 2 if x <= 12 
                     else 3 if x < 24 
                     else 4 if x <= 48 
                     else 5 if x <= 108 
                     else 6 if x <= 168
                     else 7 if x <= 228
                     else "Adulto" 
                     for x in datos["EDAD_MESES"]]


