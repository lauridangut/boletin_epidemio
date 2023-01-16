#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:21:04 2023

@author: usuario
"""

#Importación de librerías y paquetes
import streamlit as st
import pandas as pd
import epiweeks
import datetime
from epiweeks import Week, Year
import numpy as np
import matplotlib as plt
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
import os
import glob

#Título de la página
st.set_page_config(
    page_title="Aplicación para la vigilancia epidemiológica de los Virus Respiratorios",
    page_icon="/home/usuario/Downloads/Laura/boletin_epidemio/img/virus.png", 
    layout="wide"
    )

#Barra lateral
st.sidebar.markdown('# Unidad de Virología y Epidemiología Molecular')
st.sidebar.image(
    '/home/usuario/Downloads/Laura/boletin_epidemio/img/logo_garrahan.png', width=200)

#Principal
st.header("Servicio de Microbiología - Hospital de Pediatría S.A.M.I.C. 'Prof. Dr. Juan P. Garrahan'")


# Importación de datasets (OJO CON LOS PATH. HABRÁ QUE VER DÓNDE CARGAR LOS DATOS A ANALIZAR)
os.chdir("/home/usuario/Downloads/Laura/PARA_LAU-20220412T150430Z-001/PARA_LAU/2022 CRUDOS-20220614T142637Z-001")
lista_nombres_frames = glob.glob('RESULTADOS *.CSV') # * comodin para buscar
lista_frames = []
for archivo in lista_nombres_frames:
    datos = pd.read_csv(archivo, sep=";", encoding="ISO-8859-1")
    lista_frames.append(datos)
datos = pd.concat(lista_frames, join="inner", ignore_index=True)

# Tratamiento de los datos

# Quedarme con las filas que sí o sí contengan el dato de fecha de muestra
datos = datos[datos['FECHA_REC'].notna()]

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

    
# Filtrar por tipo de muestras (quedarse sólo con las muestras respiratorias)
muestras = ["ANF", "HISOPADO NASOFARINGEO", "LAVADO BRONCOALVEOLAR", "ASPIRADO TRAQUEAL", "BAL", "SECRECION RESPIRATORIA", "MICROBIOLOGIA", "HISOPADO FARINGEO", "Aspirado Traqueal"]
datos_resp = datos.loc[datos["TIPO_MUESTRA"].isin(muestras)]

# Ordenar por determinación para facilitar visualización
datos_resp = datos_resp.sort_values(["DET_CODIGO_1", "SEMANA_EPI"])

# Homogeneizar mayúsculas y minúsculas
datos_resp['DET_RESULTADO_1'] = datos_resp['DET_RESULTADO_1'].str.upper()

# Homogeneizar los resultados en una sola columna
datos_resp["RESULTADO"]=""
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="1111") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Adenovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="2021") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Enterovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="ADVRES") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Adenovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="COVID_R") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Pancoronavirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAC01") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "SARS-CoV-2"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR02") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus 299E"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR03") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus HKU1"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR04") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus NL63"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR05") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus OC43"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR07") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Rhinovirus/Enterovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR13") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 1"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR14") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 2"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR15") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 3"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR16") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 4"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="FAR17") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "VSR"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="INFABT") & (datos_resp["DET_RESULTADO_1"]=="INFLUENZA A")] = "Influenza A"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="INFABT") & (datos_resp["DET_RESULTADO_1"]=="INFLUENZA B")] = "Influenza B"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="MYRVD") & (datos_resp["DET_RESULTADO_1"]=="RHINOVIRUS")] = "Rhinovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="MYRVD") & (datos_resp["DET_RESULTADO_1"]=="METAPNEUMOVIRUS")] = "Metapneumovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="MYRVD") & (datos_resp["DET_RESULTADO_1"]=="METAPNEUMOVIRUS Y RHINOVIRUS")] = "Metapneumovirus y Rhinovirus"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="PANFLUR") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Panparainfluenza"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="PCR_C2") & (datos_resp["DET_RESULTADO_1"]=="DETECTADO")] = "SARS-CoV-2"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="VSR_RES") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "VSR"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="IFNABR") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Detectable"
datos_resp["RESULTADO"].loc[(datos_resp["DET_CODIGO_1"]=="MYRR") & (datos_resp["DET_RESULTADO_1"]=="DETECTABLE")] = "Detectable"
datos_resp["RESULTADO"].loc[(datos_resp["DET_RESULTADO_1"]=="NO DETECTABLE")] = "No detectable"
datos_resp["RESULTADO"].loc[(datos_resp["DET_RESULTADO_1"]=="NO DETECTADO")] = "No detectable"

# Eliminar filas duplicadas (virus que tienen conflicto: metapneumo/rhino, flu)
datos_resp_drop = datos_resp.drop(datos_resp[datos_resp["RESULTADO"]=="Detectable"].index)

# Eliminar filas sin resultado
datos_resp_drop = datos_resp_drop[datos_resp_drop.RESULTADO!=""]

# Cambiar el código de estudio (DET_CODIGO_1) de los virus con conflicto
datos_resp_drop["DET_CODIGO_1"].loc[(datos_resp_drop["DET_CODIGO_1"] == "INFABT")] = "INFAYB"
datos_resp_drop["DET_CODIGO_1"].loc[(datos_resp_drop["DET_CODIGO_1"] == "IFNABR")] = "INFAYB"
datos_resp_drop["DET_CODIGO_1"].loc[(datos_resp_drop["DET_CODIGO_1"] == "MYRR")] = "MYR"
datos_resp_drop["DET_CODIGO_1"].loc[(datos_resp_drop["DET_CODIGO_1"] == "MYRVD")] = "MYR"

### Análisis de los datos
## Número y características de pacientes estudiados 
pacientes_estudiados = datos_resp_drop.groupby(["PAC_ID", "CAT_EDAD", "SEXO"]).size().to_frame()
pacientes_estudiados.rename(columns={0:"CANT_DET"}, inplace=True)
pacientes_estudiados.reset_index(inplace=True)
print(len(pacientes_estudiados))

# Número de pacientes estudiados por categoría de edad
pac_est_edad = pacientes_estudiados.groupby(["CAT_EDAD"]).agg("count")
pac_est_edad.rename(columns={"CANT_DET": "CANT_EDAD"}, inplace=True)
pac_est_edad["PORCENTAJE"] = 0
print(pac_est_edad["CANT_EDAD"].sum())

# Porcentaje de pacientes estudiados por categoría de edad
for i in range(0, len(pac_est_edad)):
    porcentaje = round(pac_est_edad["CANT_EDAD"].iloc[i]*100/len(pacientes_estudiados), 1) 
    pac_est_edad["PORCENTAJE"].iloc[i] = porcentaje

# Dataframe SOLO PEDIATRICOS
pediatricos = [1, 2, 3, 4, 5, 6, 7]
solo_ped = datos_resp_drop[datos_resp_drop["CAT_EDAD"].isin(pediatricos)]
## Número y características de pacientes estudiados 
pacientes_ped_estudiados = solo_ped.groupby(["PAC_ID", "CAT_EDAD", "SEXO"]).size().to_frame()
pacientes_ped_estudiados.rename(columns={0:"CANT_DET"}, inplace=True)
pacientes_ped_estudiados.reset_index(inplace=True)
print(len(pacientes_ped_estudiados))
# Número de pacientes pediatricos estudiados por categoría de edad
pac_ped_edad = pacientes_ped_estudiados.groupby(["CAT_EDAD"]).agg("count")
pac_ped_edad.rename(columns={"CANT_DET": "CANT_EDAD"}, inplace=True)
pac_ped_edad["PORCENTAJE"] = 0
print(pac_ped_edad["CANT_EDAD"].sum())
# Porcentaje de pacientes pediatricos estudiados por categoría de edad
for i in range(0, len(pac_ped_edad)):
    porcentaje = round(pac_ped_edad["CANT_EDAD"].iloc[i]*100/len(pacientes_ped_estudiados), 1) 
    pac_ped_edad["PORCENTAJE"].iloc[i] = porcentaje

# Dataframe SOLO ADULTOS
solo_adultos = datos_resp_drop[datos_resp_drop["CAT_EDAD"] == "Adulto"]
adultos_estudiados = solo_adultos.groupby(["PAC_ID", "CAT_EDAD", "SEXO"]).size().to_frame()
adultos_estudiados.rename(columns={0:"CANT_DET"}, inplace=True)
adultos_estudiados.reset_index(inplace=True)
print(len(adultos_estudiados))
    
# Número de pacientes estudiados por sexo
pac_est_sexo = pacientes_estudiados.groupby(["SEXO"]).agg("count")
pac_est_sexo.rename(columns={"CANT_DET": "CANT_SEXO"}, inplace=True)
pac_est_sexo["PORCENTAJE"] = 0
# Porcentaje de pacientes estudiados por sexo
for i in range(len(pac_est_sexo)):
    porcentaje = round(pac_est_sexo["CANT_SEXO"].iloc[i]*100/len(pacientes_estudiados), 2)   
    pac_est_sexo["PORCENTAJE"].iloc[i] = porcentaje

# Número de pacientes estudiados por sexo y categoría de edad
pac_est_sexo_edad = pacientes_estudiados.groupby(["SEXO", "CAT_EDAD"]).agg("count")
pac_est_sexo_edad.rename(columns={"CANT_DET": "CANT"}, inplace=True)   
pac_est_sexo_edad.reset_index(inplace=True)
pac_est_sexo_edad = pac_est_sexo_edad.pivot(index="CAT_EDAD", columns="SEXO", values="CANT")
pac_est_sexo_edad.reset_index(inplace=True)

pac_est_sexo_edad["EDAD"] = ["< 6 meses" if x == 1
                     else "6 a 12 meses" if x == 2 
                     else "13 a 23 meses" if x == 3 
                     else "2 a 4 años" if x == 4 
                     else "5 a 9 años" if x == 5 
                     else "10 a 14 años" if x == 6
                     else "15 a 19 años" if x == 7
                     else "Adulto" 
                     for x in pac_est_sexo_edad["CAT_EDAD"]]
     
# Gráfico población estudiada (sexo y edad)
y_edad = pac_est_sexo_edad["EDAD"]
x_M = pac_est_sexo_edad["M"]
x_F = pac_est_sexo_edad["F"] * -1
fig = go.Figure()
fig.add_trace(go.Bar(y= y_edad, x = x_M, 
                     name = "Varones", 
                     orientation = "h"))
fig.add_trace(go.Bar(y = y_edad, x = x_F,
                     name = "Mujeres", 
                     orientation = "h"))
fig.update_layout(title = "POBLACIÓN ESTUDIADA POR CATEGORÍA DE EDAD",
                 title_font_size = 20, barmode = 'relative',
                 bargap = 0.0, bargroupgap = 0,
                 xaxis = dict(tickvals = [-3000, -2000, -1000, -500,
                                          0, 500, 1000, 2000, 3000],
                                
                              ticktext = ["3000", "2000", "1000", "500", 
                                          "0", "500", "1000", "2000", "3000"],
                              title = "Total estudiados",
                              title_font_size = 20),
                 yaxis = dict(title= "Categoría de Edad",
                              title_font_size = 20),
                 font=dict(size=20,
                             )
                 )
fig.update_yaxes(type='category')
fig.write_image("poblacion_acum.png", scale=2)
fig.show()

# Mediana de edad y rango, moda (categoría de edad). General
mediana = datos_resp_drop["EDAD_AÑOS"].median()
print(mediana)
moda = datos_resp_drop["CAT_EDAD"].mode()
print(moda)
maximo = datos_resp_drop["EDAD_AÑOS"].max()  
print(maximo)
minimo = datos_resp_drop["EDAD_AÑOS"].min()
print(minimo)

# Mediana de edad y rango, moda (categoría de edad). Pediatricos
mediana = solo_ped["EDAD_AÑOS"].median()
print(mediana)
moda = solo_ped["CAT_EDAD"].mode()
print(moda)
maximo = solo_ped["EDAD_AÑOS"].max()  
print(maximo)
minimo = solo_ped["EDAD_AÑOS"].min()
print(minimo)

## Número de muestras procesadas
muestras_proc = datos_resp_drop.groupby(["NUMERO"]).size().to_frame()
muestras_proc.rename(columns={0:"CANT_DET"}, inplace=True)
print(len(muestras_proc))
cant_det = muestras_proc["CANT_DET"].sum()
print(cant_det)
