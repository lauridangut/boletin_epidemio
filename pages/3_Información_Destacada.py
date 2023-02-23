#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:21:04 2023

@author: usuario
"""

#Importación de librerías y paquetes
# import numpy as np
# import matplotlib as plt
# pd.options.plotting.backend = "plotly"
# import chart_estudio.plotly as py
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio
# import plotly.express as px
# import plotly.figure_factory as ff
# pio.renderers.default='browser'
# import seaborn as sns
# from pandas.api.types import CategoricalDtype
# import dateutil.parser
# import os
# import glob

#Título de la página
import streamlit as st
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

#Header
st.title("Carga de datos y primeros análisis")

# Obtener una lista de archivos csv seleccionados por el usuario, leer los archivos, concatenarlos y hacer limpieza de los datos

import pandas as pd
files = st.file_uploader(
  'Seleccione los archivos .csv a analizar',
  type="csv",
  accept_multiple_files=True,
  )
if files:
    dataset = pd.concat([pd.read_csv(file, sep=";",encoding=("ISO-8859-1")) for file in files], join="inner", ignore_index=True)
    # Tratamiento de los datos
    ## Quedarme con las filas que sí o sí contengan el dato de fecha de muestra
    dataset = dataset[dataset['FECHA_REC'].notna()]
    ## Dar formato de fecha a "FECHA_NACIMIENTO" y "FECHA_REC"
    # # =============================================================================
    # # OJOOOOOO!!! LAS FECHAS DE LOS CSV DEBEN TENER EL MISMO FORMATO 
    # # =============================================================================
    import datetime
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
             st.warning("Error en formato fecha. Cargar archivo CRUDO ", fecha)

    for i in range(0, len(dataset)):
        dataset.FECHA_REC.iloc[i] = asign_fecha(dataset.FECHA_REC.iloc[i])

    for i in range(0, len(dataset)):
        dataset.FECHA_NACIMIENTO.iloc[i] = asign_fecha(dataset.FECHA_NACIMIENTO.iloc[i])
        
    # Agregar columna de semana epidemiológica
    from epiweeks import Week
    for i in range(0, len(dataset)):
        fecha = dataset["FECHA_REC"].iloc[i]
        dataset.at[i,"SEMANA_EPI"] = Week.fromdate(fecha, system="CDC")
        del(fecha, i)

    # Agregar columna de edad en meses
    from dateutil.relativedelta import relativedelta as rd
    dataset["EDAD_MESES"] = dataset.apply(lambda x: rd(x["FECHA_REC"],x["FECHA_NACIMIENTO"]).years * 12 + rd(x["FECHA_REC"],x["FECHA_NACIMIENTO"]).months, axis=1)

    # Agregar columna de edad en años
    dataset["EDAD_AÑOS"] = dataset.apply(lambda x: rd(x["FECHA_REC"], x["FECHA_NACIMIENTO"]).years, axis=1)
    

    # Agregar columna categoría de edad (list comprehension):
        # 1 < 6 meses
        # 2 = 6 a 11 meses
        # 3 = 11 a 23 meses
        # 4 = 24 a 48 meses
        # 5 = 49 a 108 meses
        # 6 = 109 a 168 meses
        # 7 = 169 a 228 meses
    dataset["CAT_EDAD"] = [1 if x < 6
                          else 2 if x <= 12 
                          else 3 if x < 24 
                          else 4 if x <= 48 
                          else 5 if x <= 108 
                          else 6 if x <= 168
                          else 7 if x <= 228
                          else "Adulto" 
                          for x in dataset["EDAD_MESES"]]
    ## Filtrar por tipo de muestras (quedarse sólo con las muestras respiratorias)
    muestras = ["ANF", "HISOPADO NASOFARINGEO", "LAVADO BRONCOALVEOLAR", "ASPIRADO TRAQUEAL", "BAL", "SECRECION RESPIRATORIA", "MICROBIOLOGIA", "HISOPADO FARINGEO", "Aspirado Traqueal"]
    dataset = dataset[dataset["TIPO_MUESTRA"].isin(muestras)]
    ## Homogeneizar mayúsculas y minúsculas
    dataset['DET_RESULTADO_1'] = dataset['DET_RESULTADO_1'].str.upper()
    ## Homogeneizar los resultados en una sola columna
    dataset["RESULTADO"]=""
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="1111") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Adenovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="2021") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Enterovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="ADVRES") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Adenovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="COVID_R") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Pancoronavirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAC01") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "SARS-CoV-2"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR02") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus 299E"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR03") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus HKU1"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR04") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus NL63"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR05") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Coronavirus OC43"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR07") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Rhinovirus/Enterovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR13") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 1"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR14") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 2"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR15") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 3"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR16") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "Parainfluenza 4"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="FAR17") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "VSR"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="INFABT") & (dataset["DET_RESULTADO_1"]=="INFLUENZA A")] = "Influenza A"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="INFABT") & (dataset["DET_RESULTADO_1"]=="INFLUENZA B")] = "Influenza B"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="MYRVD") & (dataset["DET_RESULTADO_1"]=="RHINOVIRUS")] = "Rhinovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="MYRVD") & (dataset["DET_RESULTADO_1"]=="METAPNEUMOVIRUS")] = "Metapneumovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="MYRVD") & (dataset["DET_RESULTADO_1"]=="METAPNEUMOVIRUS Y RHINOVIRUS")] = "Metapneumovirus y Rhinovirus"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="PANFLUR") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Panparainfluenza"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="PCR_C2") & (dataset["DET_RESULTADO_1"]=="DETECTADO")] = "SARS-CoV-2"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="VSR_RES") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "VSR"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="IFNABR") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Detectable"
    dataset["RESULTADO"].loc[(dataset["DET_CODIGO_1"]=="MYRR") & (dataset["DET_RESULTADO_1"]=="DETECTABLE")] = "Detectable"
    dataset["RESULTADO"].loc[(dataset["DET_RESULTADO_1"]=="NO DETECTABLE")] = "No detectable"
    dataset["RESULTADO"].loc[(dataset["DET_RESULTADO_1"]=="NO DETECTADO")] = "No detectable"
    ## Eliminar filas duplicadas (virus que tienen conflicto: metapneumo/rhino, flu)
    dataset = dataset.drop(dataset[dataset["RESULTADO"]=="Detectable"].index)
    ## Eliminar filas sin resultado
    dataset = dataset[dataset.RESULTADO!=""]
    ## Cambiar el código de estudio (DET_CODIGO_1) de los virus con conflicto
    dataset["DET_CODIGO_1"].loc[(dataset["DET_CODIGO_1"] == "INFABT")] = "INFAYB"
    dataset["DET_CODIGO_1"].loc[(dataset["DET_CODIGO_1"] == "IFNABR")] = "INFAYB"
    dataset["DET_CODIGO_1"].loc[(dataset["DET_CODIGO_1"] == "MYRR")] = "MYR"
    dataset["DET_CODIGO_1"].loc[(dataset["DET_CODIGO_1"] == "MYRVD")] = "MYR"
    ## Ordenar por determinación para facilitar visualización
    dataset = dataset.sort_values(["DET_CODIGO_1", "SEMANA_EPI"])
    st.write(dataset)
    # # Descargar el archivo
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    dataframe=dataset.copy()
    dataset = convert_df(dataset)
    
    st.download_button(
        label="Descargar archivo procesado",
        data=dataset,
        file_name='archivo_procesado.csv',
        mime='text/csv',
    )
    ### Análisis de los datos
    # Cantidad de determinaciones hechas
    cantidad_determinaciones = len(dataframe)
    # Cantidad de pacientes estudiados
    cant_pac_estudiados = dataframe["PAC_ID"].nunique()
    # Cantidad de determinaciones positivas
    cantidad_positivos = len(dataframe[dataframe["RESULTADO"] != "No detectable"])
    # Porcentaje de determinaciones positivas
    porcentaje_pos = round((cantidad_positivos*100)/cantidad_determinaciones,1)
    # Widget métricas
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2 = st.columns(2)
    col1.metric(label="Cantidad de determinaciones realizadas", value=cantidad_determinaciones)
    col2.metric(label="Cantidad de pacientes estudiados", value=cant_pac_estudiados)
    col3, col4 = st.columns(2)
    col3.metric(label="Cantidad de determinaciones positivas", value=cantidad_positivos)
    col4.metric(label="Porcentaje de positividad total (%)", value=porcentaje_pos)
    style_metric_cards(border_left_color="#B86EE6")
    # Número y características de pacientes estudiados 
    pacientes_estudiados = dataframe.groupby(["PAC_ID", "CAT_EDAD", "SEXO"]).size().to_frame()
    pacientes_estudiados.rename(columns={0:"CANT_DET"}, inplace=True)
    pacientes_estudiados.reset_index(inplace=True)
    # Número de pacientes estudiados por categoría de edad
    pac_est_edad = pacientes_estudiados.groupby(["CAT_EDAD"]).agg("count")
    pac_est_edad.rename(columns={"CANT_DET": "CANT_EDAD"}, inplace=True)
    pac_est_edad["PORCENTAJE"] = 0
    pac_est_edad["CANT_EDAD"].sum()
    # Porcentaje de pacientes estudiados por categoría de edad
    for i in range(0, len(pac_est_edad)):
        porcentaje = (pac_est_edad["CANT_EDAD"].iloc[i]*100)/len(pacientes_estudiados) 
        pac_est_edad["PORCENTAJE"].iloc[i] = round(porcentaje)
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
    edad_dict = {"1": "< 6 meses", "2": "6 a 12 meses", "3": "13 a 23 meses", "4": "2 a 4 años",
                 "5": "5 a 9 años", "6": "10 a 14 años", "7": "15 a 19 años", "8": "Adulto"}
    pac_est_sexo_edad["EDAD"] = pac_est_sexo_edad["CAT_EDAD"].replace(edad_dict)

    # Gráfico población estudiada (sexo y edad)
    import plotly.graph_objects as go
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
    fig.update_layout(title = "POBLACIÓN ESTUDIADA POR EDAD",
                      title_font_size = 20, barmode = 'relative',
                      bargap = 0.0, bargroupgap = 0,
                      xaxis = dict(tickvals = [-3000, -2000, -1000, -500,
                                              0, 500, 1000, 2000, 3000],
                                    
                                  ticktext = ["3000", "2000", "1000", "500", 
                                              "0", "500", "1000", "2000", "3000"],
                                  title = "Total estudiados",
                                  title_font_size = 20),
                      yaxis = dict(title= "Edad",
                                  title_font_size = 20),
                      font=dict(size=20,
                                  )
                      )
    fig.update_yaxes(type='category')
    fig.write_image("poblacion_acum.png", scale=2)
    st.plotly_chart(fig)

    # Dataframe SOLO PEDIATRICOS
    excluir_adultos = ["Adulto"]
    solo_ped = dataframe[~dataframe["CAT_EDAD"].isin(excluir_adultos)]
    st.write(solo_ped)
    ## Número y características de pacientes estudiados 
    pacientes_ped_estudiados = solo_ped.groupby(["PAC_ID", "CAT_EDAD", "SEXO"]).size().to_frame()
    pacientes_ped_estudiados.rename(columns={0:"CANT_DET"}, inplace=True)
    pacientes_ped_estudiados.reset_index(inplace=True)
    # st.write(pacientes_ped_estudiados)
    # Número de pacientes pediatricos estudiados por categoría de edad
    pac_ped_edad = pacientes_ped_estudiados.groupby(["CAT_EDAD"]).agg("count")
    pac_ped_edad.rename(columns={"CANT_DET": "CANT_EDAD"}, inplace=True)
    pac_ped_edad["PORCENTAJE"] = 0
    # Porcentaje de pacientes pediatricos estudiados por categoría de edad
    for i in range(0, len(pac_ped_edad)):
        porcentaje = round(pac_ped_edad["CANT_EDAD"].iloc[i]*100/len(pacientes_ped_estudiados), 1) 
        pac_ped_edad["PORCENTAJE"].iloc[i] = porcentaje
    ## Mediana de edad y rango, moda (categoría de edad). Pediatricos
    mediana = solo_ped["EDAD_AÑOS"].median()
    moda = solo_ped["EDAD_AÑOS"].mode()
    maximo = solo_ped["EDAD_AÑOS"].max()  
    minimo = solo_ped["EDAD_AÑOS"].min()
    st.subheader("Mediana de Edad en años de Pacientes Pediátricos estudiados:", anchor=None)
    st.write(mediana)
    st.subheader("Moda de Edad en años de Pacientes Pediátricos estudiados:", anchor=None)
    st.write(moda[0])
    st.subheader("Rango de Edad en años de Pacientes Pediátricos estudiados (min):", anchor=None)
    st.write(minimo)
    st.subheader("Rango de Edad en años de Pacientes Pediátricos estudiados (máx):", anchor=None)
    st.write(maximo)
    # Boxplot población pediátrica estudiada (sexo y edad) para representar mediana y rangos 
    import plotly.express as px
    boxplot = px.box(solo_ped, x='SEXO', y="EDAD_AÑOS")
    st.plotly_chart(boxplot)
    # Tabla: Cantidad de determinaciones realizadas por estudio
    st.subheader("Total de determinaciones realizadas por estudio (Pediátricos y Adultos acompañantes)")
    determinaciones_por_estudio = dataframe.groupby(["DET_CODIGO_1"]).size().to_frame()
    determinaciones_por_estudio.rename(columns={0: "DETERMINACIONES REALIZADAS"}, inplace=True)
    determinaciones_por_estudio.reset_index(inplace=True)
    determinaciones_por_estudio.rename(columns={"DET_CODIGO_1": "VIRUS (MÉTODO)"}, inplace=True)
    determinaciones_por_estudio["VIRUS (MÉTODO)"] = determinaciones_por_estudio["VIRUS (MÉTODO)"].replace({"1111":"Adenovirus (PCR)", "2021":"Enterovirus (PCR)",
                    "ADVRES":"Adenovirus (Determinación y/o carga)",
                    "COVID_R":"Pancoronavirus (PCR)",
                    "FAC01":"SARS-CoV-2 (PCR)",
                    "FAR02":"Coronavirus 299E (Filmarray)",
                    "FAR03":"Coronavirus HKU1 (Filmarray)",
                    "FAR04":"Coronavirus NL63 (Filmarray)",
                    "FAR05":"Coronavirus OC43 (Filmarray)",
                    "FAR07":"Rhinovirus/Enterovirus (Filmarray)",
                    "FAR13":"Parainfluenza 1 (Filmarray)",
                    "FAR14":"Parainfluenza 2 (Filmarray)",
                    "FAR15":"Parainfluenza 3 (Filmarray)",
                    "FAR16":"Parainfluenza 4 (Filmarray)",
                    "FAR17":"Virus Respiratorio Sincicial (Filmarray)",
                    "INFAYB":"Virus Influenza A y B (PCR)",
                    "MYR":"Metapneumovirus y Rhinovirus (PCR)",
                    "PANFLUR":"Panparainfluenza (PCR)",
                    "PCR_C2":"SARS-CoV-2 (Filmarray)",
                    "VSR_RES":"Virus Respiratorio Sincicial (PCR)"})
    st.write(determinaciones_por_estudio)    
    # Barplot: Cantidad de determinaciones realizadas por estudio (pediátricos y adultos)
    st.subheader("Total de determinaciones vs Estudio (Pediátricos y Adultos acompañantes)")
    fig = px.bar(determinaciones_por_estudio, y='DETERMINACIONES REALIZADAS', x='VIRUS (MÉTODO)', text='DETERMINACIONES REALIZADAS')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)
    
    # Tabla: Pediátricos Positivos
    lista_positivos = ["Adenovirus", "Enterovirus", "Pancoronavirus", "SARS-CoV-2", "Coronavirus 299E", "Coronavirus HKU1", "Coronavirus NL63", "Coronavirus OC43", "Rhinovirus/Enterovirus",  "Parainfluenza 1", "Parainfluenza 2", "Parainfluenza 3", "Parainfluenza 4", "VSR", "Influenza A", "Influenza B", "Rhinovirus", "Metapneumovirus", "Panparainfluenza", "Metapneumovirus y Rhinovirus"]
    positivos = solo_ped[solo_ped["RESULTADO"].isin(lista_positivos)]
    st.subheader("Pacientes Pediátricos con Infección Viral Respiratoria")
    st.write(positivos)
    
    # Barplot: Número de determinaciones positivas (filtrar columna RESULTADO y quedarme con todo lo que no sea No detectable). Sólo PEDIÁTRICOS
    st.subheader("Estudio vs Determinaciones: Pacientes Pediátricos.")
    import plotly.graph_objects as go
    value_counts = positivos['ESTUDIO'].value_counts()
    estudio = value_counts.index
    counts = value_counts.values
    
    totales = solo_ped["ESTUDIO"].value_counts()
    estudio_totales = totales.index
    counts_totales = totales.values
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=estudio,
        y=counts,
        name='Positivos',
        marker_color='indianred'
    ))
    
    fig.add_trace(go.Bar(
        x=estudio_totales,
        y=counts_totales,
        name='Total de determinaciones',
        marker_color='lightsalmon'
    ))
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    st.plotly_chart(fig)
    
    # Diccionarios de color:
    color_list = ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52', '#FF6E8D', '#9BBC6B', '#FFD54F', '#A0836C', '#F29B76', '#8390FA', '#9CBAA9', '#D1B993', '#B2B2B2', '#EEDD82', '#CCCCCC']

    color_dict = {"Adenovirus": color_list[0], "Enterovirus": color_list[1], "Pancoronavirus": color_list[2], "SARS-CoV-2": color_list[3], "Coronavirus 299E": color_list[4], "Coronavirus HKU1": color_list[5], "Coronavirus NL63": color_list[6], "Coronavirus OC43": color_list[7], "Rhinovirus/Enterovirus": color_list[8], "Parainfluenza 1": color_list[9], "Parainfluenza 2": color_list[10], "Parainfluenza 3": color_list[11], "Parainfluenza 4": color_list[12], "VSR": color_list[13], "Influenza A": color_list[14], "Influenza B": color_list[15], "Rhinovirus": color_list[16], "Metapneumovirus": color_list[17], "Panparainfluenza": color_list[18], "Metapneumovirus y Rhinovirus": color_list[19], "No detectable": color_list[20]}


    
    # Piechart: Distribución de virus respiratorios en muestras positivas. Sólo PEDIÁTRICOS.
    st.subheader("Distribución de virus respiratorios en el total de muestras positivas de pacientes pediátricos")
    pos_torta = positivos["RESULTADO"].value_counts()
    st.write(pos_torta)
    fig = px.pie(positivos, values=pos_torta, names=pos_torta.index, color=pos_torta.index, color_discrete_map=color_dict)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig)

    # Barplot Semana epidemiológica vs cantidad de casos positivos
    st.subheader("Semana epidemiológica vs cantidad de casos positivos: pacientes pediátricos")
    filtro_negativos = solo_ped[solo_ped["RESULTADO"] != "No detectable"]
    filtro_negativos['Semana Epidemiológica'] = filtro_negativos['SEMANA_EPI'].astype(str).str[-2:]
    barplot = filtro_negativos.groupby('Semana Epidemiológica')['RESULTADO'].value_counts().reset_index(name='count')
    barplot.rename(columns={"count": "Cantidad de casos"}, inplace=True)
    st.write(barplot)
    fig = px.bar(barplot, x="Semana Epidemiológica", y="Cantidad de casos", color= "RESULTADO", title="Cantidad de Casos por Semana Epidemiológica", color_discrete_map=color_dict)
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1))
    st.plotly_chart(fig)
   
    # Tabla para graficar Semana epidemiológica vs porcentaje de positividad de cada virus
    st.subheader("Dataframe para graficar Semana epidemiológica vs porcentaje de positividad: pacientes pediátricos")
    temp_df = solo_ped.groupby(["ESTUDIO", "SEMANA_EPI", "RESULTADO"]).count().reset_index()
    temp_df = temp_df[["ESTUDIO", "SEMANA_EPI", "RESULTADO", "FECHA_REC"]]
    temp_df.rename(columns={"FECHA_REC": "Cantidad"}, inplace=True)
    temp_df['SEMANA_EPI'] = temp_df['SEMANA_EPI'].astype(str).str[-2:]
    temp_df['ESTUDIO'].replace(['ADENOVIRUS POR PCR', 'ADV: DETERMINACIÓN Y/O CARGA'], 'ADENOVIRUS', inplace=True)
    temp_df_sum = temp_df.groupby(["ESTUDIO", "SEMANA_EPI"])["Cantidad"].sum().reset_index()
    temp_df = pd.merge(temp_df, temp_df_sum, on=["ESTUDIO", "SEMANA_EPI"], how="left")
    temp_df.rename(columns={"Cantidad_x": "Cantidad", "Cantidad_y": "Total Estudiados", "SEMANA_EPI": "Semana Epidemiológica"}, inplace=True)
    temp_df["Porcentaje"] = round(temp_df["Cantidad"]/temp_df["Total Estudiados"]*100, 1)

    
     #Solucionar desagrupamiento de adenovirus

    
    
    
    
    
    
    st.write(temp_df)
    
    # Barplot Semana epidemiológica vs porcentaje de positividad de cada virus
    st.subheader("Semana epidemiológica vs porcentaje de positividad: pacientes pediátricos")
    filtro_nodetectables = temp_df[temp_df["RESULTADO"] != "No detectable"]
    filtro_nodetectables.rename(columns={"Porcentaje":"Porcentaje de Positividad"}, inplace=True)
    fig = px.bar(filtro_nodetectables, x="Semana Epidemiológica", y="Porcentaje de Positividad", color= "RESULTADO", color_discrete_map=color_dict, title="Porcentaje de Positividad por Semana Epidemiológica")
    fig.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1))
    st.plotly_chart(fig)
    

    
    
    # Agregar análisis estadísticos: analizar si hay diferencias significativas en la misma semana entre los diferentes virus y además analizar si hay diferencias significativas entre semanas epidemiológicas siguiendo un mismo virus (estacionalidad de los virus respiratorios)
    # Positivos por edad
    # Coinfectados
    # Infecciones Recurrentes
else:
    st.warning("Seleccione al menos un archivo .csv")
 

# # Tabla categorías de edad
# cat_edad = {
#          "Categoría de Edad": ["1", "2", "3", "4", "5", "6", "7", "Adulto"],
#          "Edad": ["< 6 meses", "6 a 12 meses", "13 a 23 meses", "2 a 4 años", "5 a 9 años", "10 a 14 años", "15 a 19 años", "> 19 años"]
#           }
# cat_edad = pd.DataFrame(cat_edad)

# fig =  ff.create_table(cat_edad)
# fig.update_layout(
#     autosize=False,
#     width=500,
#     height=200,
# )
# fig.write_image("table_plotly.png", scale=2)
# fig.show()

# # Tabla cantidad de determinaciones por estudio
# fig =  ff.create_table(determinaciones_por_estudio)
# fig.update_layout(
#     autosize=False,
#     width=800,
#     height=600,
# )
# fig.write_image("muestras_proc_est_acum.png", scale=2)
# fig.show()

# print(determinaciones_por_estudio["DETERMINACIONES REALIZADAS"].sum())

# # Número de determinaciones positivas (filtrar columna DET_RESULTADO_1 y quedarme con todo lo que no sea No detectado o No detectable)
# det_positivas = datos_resp_drop[(datos_resp_drop["RESULTADO"] == "Adenovirus") |
#                                (datos_resp_drop["RESULTADO"] == "Enterovirus") |
#                                (datos_resp_drop["RESULTADO"] == "Pancoronavirus") |
#                                (datos_resp_drop["RESULTADO"] == "SARS-CoV-2") |
#                                (datos_resp_drop["RESULTADO"] == "Coronavirus 299E") |
#                                (datos_resp_drop["RESULTADO"] == "Coronavirus HKU1") |
#                                (datos_resp_drop["RESULTADO"] == "Coronavirus NL63") |
#                                (datos_resp_drop["RESULTADO"] == "Coronavirus OC43") |
#                                (datos_resp_drop["RESULTADO"] == "Rhinovirus/Enterovirus") |
#                                (datos_resp_drop["RESULTADO"] == "Parainfluenza 1") |
#                                (datos_resp_drop["RESULTADO"] == "Parainfluenza 2") |
#                                (datos_resp_drop["RESULTADO"] == "Parainfluenza 3") |
#                                (datos_resp_drop["RESULTADO"] == "Parainfluenza 4") |
#                                (datos_resp_drop["RESULTADO"] == "VSR") |
#                                (datos_resp_drop["RESULTADO"] == "Influenza A") |
#                                (datos_resp_drop["RESULTADO"] == "Influenza B") |
#                                (datos_resp_drop["RESULTADO"] == "Rhinovirus") |
#                                (datos_resp_drop["RESULTADO"] == "Metapneumovirus") |
#                                (datos_resp_drop["RESULTADO"] == "Panparainfluenza") |
#                                (datos_resp_drop["RESULTADO"] == "Metapneumovirus y Rhinovirus")]
# print(len(det_positivas))
# det_positivas.to_csv("det_positivas_14-15-16-17-18.csv")
# # Porcentaje positivas
# print(round(len(det_positivas)*100/len(datos_resp_drop), 2))

# # Número de determinaciones negativas
# det_negativas = datos_resp_drop[(datos_resp_drop["RESULTADO"] == "No detectable")]
# print(len(det_negativas))
# # Porcentaje negativas
# print(round(len(det_negativas)*100/len(datos_resp_drop), 2))

# # Filtrar pacientes estudiados que son positivos (ojo! coinfectados cuentan doble)
# pac_positivos = det_positivas.sort_values(["PAC_ID"])
# pac_positivos.to_csv("pac_positivos_acum(6-18).csv")

# # Número de pacientes con al menos una infección respiratoria viral
# nro_positivos = len(det_positivas["PAC_ID"].unique())
# print(nro_positivos)
# # Porcentaje de pacientes con al menos una infección respiratoria viral
# print(round(nro_positivos*100/len(pacientes_estudiados), 2))