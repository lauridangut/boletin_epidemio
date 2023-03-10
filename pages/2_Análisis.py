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
from typing import Optional

def colored_header(
    label: str = "Nice title",
    description: Optional[str] = "Cool description",
    color_name: str = "#9d4edd",
):
    """
    Shows a header with a colored underline and an optional description.
    """
    st.title(label)
    st.write(
        f'<hr style="background-color: {color_name}; margin-top: 0;'
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description)
        
descripcion = "📌 Utilice el sistema informático hospitalario SIG-HG para extraer la información a analizar"
        
colored_header(
    label="Carga de datos y primeros análisis",
    description=descripcion,
    color_name="#9d4edd",
)


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
    
    # Función para ocultar los datos con asteriscos
    def ocultar_datos(valor):
        if isinstance(valor, str):
            return '*' * len(valor)
        else:
            return valor

    
    
    # Breve descripción del output
    st.caption("📌 Los archivos ingresados fueron procesados para obtener el DataFrame que se muestra a continuación. Éste contiene, a diferencia de los archivos que le dieron origen: una columna con el dato de Semana Epidemiológica, una columna con la edad de los pacientes en meses y otra con la edad en años, y una columna con la edad en categorías. Adicionalmente, se seleccionaron las filas correspondientes a muestras respiratorias, se homogeneizaron mayúsculas y minúsculas, se colocaron los resultados de las determinaciones en una única columna y se eliminaron datos duplicados y filas sin resultado.", unsafe_allow_html=False)
    
    # # Descargar el archivo
    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    dataframe=dataset.copy()
    # Aplicar la función a la columna NOMBRE_COMPLETO
    dataframe['NOMBRE_COMPLETO'] = dataframe['NOMBRE_COMPLETO'].apply(ocultar_datos)
    dataset = convert_df(dataset)
    
    # Mostrar dataframe procesado
    st.dataframe(dataframe)
    
    st.download_button(
        label="Descargar tabla",
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
    st.subheader("Algunos números...:memo:")
    st.caption("📌 A partir del DataFrame anterior, se derivan las siguientes métricas:", unsafe_allow_html=False)
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
                 "5": "> 4 a 9 años", "6": "> 9 a 14 años", "7": "> 14 a 19 años", "8": "Adulto"}
    pac_est_sexo_edad["EDAD"] = pac_est_sexo_edad["CAT_EDAD"].replace(edad_dict)

    # Gráfico población estudiada (sexo y edad)
    st.subheader("Población estudiada en función de edad y sexo")
    st.caption("📌 El siguiente gráfico muestra la distribución de la población estudiada por edad y sexo. En el eje vertical se muestra la edad y en el eje horizontal se muestra el número total de pacientes estudiados. Hay dos barras para cada edad: una para los varones y otra para las mujeres. La barra azul representa el número de varones y la barra violeta representa el número de mujeres. Pose el mouse sobre cada barra para visualizar la cantidad de pacientes estudiados. Para descargar la imagen, haga click en el ícono 📷 ('Download plot as png').", unsafe_allow_html=False)
    import plotly.graph_objects as go
    y_edad = pac_est_sexo_edad["EDAD"]
    x_M = pac_est_sexo_edad["M"]
    x_F = pac_est_sexo_edad["F"] * -1
    fig = go.Figure()
    fig.add_trace(go.Bar(y= y_edad, x = x_M, 
                          name = "Varones", 
                          orientation = "h",
                          marker_color='#89c2d9'))
    fig.add_trace(go.Bar(y = y_edad, x = x_F,
                          name = "Mujeres", 
                          orientation = "h",
                          marker_color='#9d4edd'))
    fig.update_layout(title = "POBLACIÓN ESTUDIADA POR EDAD Y SEXO",
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
    st.plotly_chart(fig)

    # Hacer un chart container para DataFrame sólo pacientes pediátricos y Características de la Población Pediátrica estudiada    
    st.subheader("Características de la Población Pediátrica estudiada")
    st.caption("📌 A continuación se visualiza un gráfico de cajas (boxplot) para representar la mediana y los rangos de edad de la población pediátrica estudiada, según sexo. Para descargar la imagen, haga click en el ícono 📷 ('Download plot as png'). Además, puede posar el mouse sobre el gráfico para visualizar información adicional. Obsérvese, también, que se crea una pestaña para el gráfico, otra para el DataFrame que contiene los datos únicamente de los pacientes pediátricos y que le da origen al boxplot y, por último, otra pestaña para descargarlo en formato CSV.", unsafe_allow_html=False)
    # Dataframe SOLO PEDIATRICOS
    # st.subheader("DataFrame sólo pacientes pediátricos")
    excluir_adultos = ["Adulto"]
    solo_ped = dataframe[~dataframe["CAT_EDAD"].isin(excluir_adultos)]
    # st.dataframe(solo_ped)

    ## Número y características de pacientes estudiados
    pacientes_ped_estudiados = solo_ped.groupby(["PAC_ID", "CAT_EDAD", "SEXO"]).size().to_frame()
    pacientes_ped_estudiados.rename(columns={0:"CANT_DET"}, inplace=True)
    pacientes_ped_estudiados.reset_index(inplace=True)
    
    
    # Número de pacientes pediatricos estudiados por categoría de edad
    pac_ped_edad = pacientes_ped_estudiados.groupby(["CAT_EDAD"]).agg("count")
    pac_ped_edad.rename(columns={"CANT_DET": "CANT_EDAD"}, inplace=True)
    pac_ped_edad["PORCENTAJE"] = 0
    
    # Porcentaje de pacientes pediatricos estudiados por categoría de edad
    for i in range(0, len(pac_ped_edad)):
        porcentaje = round(pac_ped_edad["CANT_EDAD"].iloc[i]*100/len(pacientes_ped_estudiados), 1) 
        pac_ped_edad["PORCENTAJE"].iloc[i] = porcentaje
           
    # Boxplot población pediátrica estudiada (sexo y edad) para representar mediana y rangos 
    import plotly.express as px
    
    def export_csv(df):
        csv = df.to_csv(index=False)
        return csv.encode('utf-8')


    def chart_container(data: pd.DataFrame) -> None:
        boxplot = px.box(data, x='SEXO', y='EDAD_AÑOS', color='SEXO', color_discrete_map={'F': '#9d4edd', 'M': '#89c2d9'})
        
        tabs = st.tabs(['Gráfico📈', 'Dataframe📄', 'Descargar📁'])
        
        with tabs[0]:
            st.plotly_chart(boxplot)
        
        with tabs[1]:
            st.dataframe(data)
        
        with tabs[2]:
            st.download_button('Descargar tabla', data=export_csv(data), file_name='pediatricos.csv', mime='text/csv')
    
    
    if __name__ == '__main__':
        
        # Creamos el contenedor
        chart_container(solo_ped)
        
    # Diccionario de colores para gráficos
    color_list = ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52', '#FF6E8D', '#9BBC6B', '#FFD54F', '#A0836C', '#F29B76', '#8390FA', '#9CBAA9', '#D1B993', '#B2B2B2', '#EEDD82', '#CCCCCC']

    color_dictionary = {"Adenovirus (PCR)": color_list[0], "Enterovirus (PCR)": color_list[1], "Adenovirus (Determinación y/o carga)": color_list[0] ,"Pancoronavirus (PCR)": color_list[2], "SARS-CoV-2 (PCR)": color_list[3], "Coronavirus 299E (Filmarray)": color_list[4], "Coronavirus HKU1 (Filmarray)": color_list[5], "Coronavirus NL63 (Filmarray)": color_list[6], "Coronavirus OC43 (Filmarray)": color_list[7], "Rhinovirus/Enterovirus (Filmarray)": color_list[8], "Parainfluenza 1 (Filmarray)": color_list[9], "Parainfluenza 2 (Filmarray)": color_list[10], "Parainfluenza 3 (Filmarray)": color_list[11], "Parainfluenza 4 (Filmarray)": color_list[12], "Virus Respiratorio Sincicial (Filmarray)": color_list[13], "Influenza A y B (PCR)": color_list[14], "Metapneumovirus y Rhinovirus (PCR)": color_list[19], "Panparainfluenza": color_list[18], "SARS-CoV-2 (Filmarray)": color_list[3], "Rhinovirus": color_list[16], "Virus Respiratorio Sincicial (PCR)": color_list[13]}    
    
    # DataFrame Interactivo 2: Cantidad de determinaciones realizadas por estudio
    st.subheader("Total de determinaciones realizadas por estudio")
    st.caption("📌 El siguiente DataFrame es interactivo, lo que significa que usted puede filtrar las columnas como una planilla de Excel y **seleccionar las filas que le interese visualizar en un gráfico de barras (barplot)**. Los datos utilizados para su construcción contemplan el total de pacientes estudiados, tanto pediátricos como adultos acompañantes. Igualmente que los gráficos anteriores, se puede descargar haciendo click en el ícono 📷 ('Download plot as png'). Además, puede seleccionar las barras que desea ver haciendo click en cada referencia al margen del gráfico.", unsafe_allow_html=False)
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
    # st.write(determinaciones_por_estudio)    
    
    from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
    gb = GridOptionsBuilder.from_dataframe(determinaciones_por_estudio)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()
    
    grid_response = AgGrid(
        determinaciones_por_estudio,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=True,
        theme='alpine', #Add theme color to the table
        enable_enterprise_modules=True,
        height=600, 
        width='40%',
        reload_data=True
    )
    
    data1 = grid_response['data']
    selected1 = grid_response['selected_rows'] 
    df1 = pd.DataFrame(selected1) #Pass the selected rows to a new dataframe df
    
    if selected1:
        fig = px.bar(df1, x='VIRUS (MÉTODO)', y='DETERMINACIONES REALIZADAS', color="VIRUS (MÉTODO)", color_discrete_map=color_dictionary, title="DETERMINACIONES REALIZADAS")
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig)
    # else:
    #     st.write("Seleccione las filas de la tabla que desee graficar.")
    

        
    # Tabla: Pediátricos Positivos
    st.subheader("Pacientes Pediátricos con Infección Viral Respiratoria")
    st.caption("📌 En el DataFrame que se muestra a continuación se encuentran los datos de aquellos pacientes que resultaron positivos para al menos uno de los estudios de infección respiratoria. Utilice la barra lateral del mismo para realizar filtrados de las columnas y obtener una visualización óptima.", unsafe_allow_html=False)
    lista_positivos = ["Adenovirus", "Enterovirus", "Pancoronavirus", "SARS-CoV-2", "Coronavirus 299E", "Coronavirus HKU1", "Coronavirus NL63", "Coronavirus OC43", "Rhinovirus/Enterovirus",  "Parainfluenza 1", "Parainfluenza 2", "Parainfluenza 3", "Parainfluenza 4", "VSR", "Influenza A", "Influenza B", "Rhinovirus", "Metapneumovirus", "Panparainfluenza", "Metapneumovirus y Rhinovirus"]
    positivos = solo_ped[solo_ped["RESULTADO"].isin(lista_positivos)]

    gb = GridOptionsBuilder.from_dataframe(positivos)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gridOptions = gb.build()
    
    # Mostrar la tabla AgGrid
    data_return_mode = 'AS_INPUT'
    download_filename = "pediatricos_positivos.csv"
    download_button = "Descargar tabla"
    grid_id = "my_grid"
    AgGrid(positivos, gridOptions=gridOptions, grid_id=grid_id, height=600, theme='alpine')
    
    # Crear un botón de descarga
    csv = positivos.to_csv(index=False).encode()
    st.download_button(
        label=download_button,
        data=csv,
        file_name=download_filename,
        mime="text/csv",
    )
    

    # Barplot: Número de determinaciones positivas (filtrar columna RESULTADO y quedarme con todo lo que no sea No detectable). Sólo PEDIÁTRICOS
    st.subheader("Comparación entre la cantidad de positivos y el total de determinaciones por estudio en pacientes pediátricos")
    st.caption("📌 El siguiente barplot contrasta la cantidad total de determinaciones con las positivas para cada estudio. Recuerde que puede posar el mouse sobre la figura para obtener información adicional, así como también, seleccionar las barras que se desea visualizar haciendo click en la referencia del margen. Además, puede acceder al modo fullscreen para agrandar la imagen.", unsafe_allow_html=False)
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
        marker_color="mediumorchid"
    ))
    
    fig.add_trace(go.Bar(
        x=estudio_totales,
        y=counts_totales,
        name='Total de determinaciones',
        marker_color="rebeccapurple"
    ))
    fig.update_layout(barmode='group', xaxis_tickangle=90)
    st.plotly_chart(fig, height=1200, width=1600)
    
    # Diccionarios de color:
    color_list = ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A', '#19d3f3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52', '#FF6E8D', '#9BBC6B', '#FFD54F', '#A0836C', '#F29B76', '#8390FA', '#9CBAA9', '#D1B993', '#B2B2B2', '#EEDD82', '#CCCCCC']

    color_dict = {"Adenovirus": color_list[0], "Enterovirus": color_list[1], "Pancoronavirus": color_list[2], "SARS-CoV-2": color_list[3], "Coronavirus 299E": color_list[4], "Coronavirus HKU1": color_list[5], "Coronavirus NL63": color_list[6], "Coronavirus OC43": color_list[7], "Rhinovirus/Enterovirus": color_list[8], "Parainfluenza 1": color_list[9], "Parainfluenza 2": color_list[10], "Parainfluenza 3": color_list[11], "Parainfluenza 4": color_list[12], "VSR": color_list[13], "Influenza A": color_list[14], "Influenza B": color_list[15], "Rhinovirus": color_list[16], "Metapneumovirus": color_list[17], "Panparainfluenza": color_list[18], "Metapneumovirus y Rhinovirus": color_list[19], "No detectable": color_list[20]}


    
    # Piechart: Distribución de virus respiratorios en muestras positivas. Sólo PEDIÁTRICOS.
    st.subheader("Distribución de virus respiratorios en el total de muestras positivas de pacientes pediátricos")
    st.caption("📌 A continuación se muestra un gráfico de torta, en el cual representa la distribución de los virus respiratorios encontrados entre el total de muestras positivas analizadas, tanto por PCR como por Filmarray. La finalidad es proporcionar una visión general de los agentes etiológicos responsables de la mayoría de las infecciones virales respiratorias. En otras palabras, se busca identificar los virus que causan la mayor cantidad de casos positivos en el conjunto de muestras analizadas, lo que puede ser útil para entender la epidemiología y la dinámica de las infecciones respiratorias en la población pediátrica que concurre al hospital.", unsafe_allow_html=False)
    pos_torta = positivos["RESULTADO"].value_counts().to_frame().reset_index()
    pos_torta.rename(columns={"index":"Virus", "RESULTADO": "Cantidad de casos"}, inplace=True)
    # st.dataframe(pos_torta)
    fig = px.pie(pos_torta, values='Cantidad de casos', names='Virus', color='Virus', color_discrete_map=color_dict)
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    # st.plotly_chart(fig)
    

    def chart_container(data: pd.DataFrame) -> None:
        fig = px.pie(pos_torta, values='Cantidad de casos', names='Virus', color='Virus', color_discrete_map=color_dict)
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        
        tabs = st.tabs(['Gráfico📈', 'Dataframe📄', 'Descargar📁'])
        
        with tabs[0]:
            st.plotly_chart(fig)
        
        with tabs[1]:
            st.dataframe(data)
        
        with tabs[2]:
            st.download_button('Descargar tabla', data=export_csv(data), file_name='data.csv', mime='text/csv')
    
    
    if __name__ == '__main__':
        
        # Creamos el contenedor
        chart_container(pos_torta)
        

    # Tabla para graficar Semana epidemiológica vs porcentaje de positividad de cada virus
    st.subheader("Distribución de Virus Respiratorios en función de la Semana Epidemiológica")
    st.caption("📌 El siguiente DataFrame proporciona información sobre el recuento de las determinaciones realizadas y los resultados de los pacientes pediátricos estudiados, así como la semana epidemiológica en la que se tomaron las muestras. A partir de esta información, se calcula el porcentaje de positividad para cada uno de los virus. Esta tabla cuenta con una barra lateral con opciones para seleccionar columnas y filtrar datos. Además, seleccionando las filas de interés, se puede generar un gráfico de barras donde el eje horizontal representa la Semana Epidemiológica y el eje vertical el Porcentaje de Positividad. Los datos se presentan de forma interactiva, permitiendo a los usuarios obtener información adicional pasando el cursor sobre la figura y filtrando la imagen haciendo clic en las referencias del margen. Podría ser valioso, por ejemplo, visualizar individualmente algún virus en particular utilizando esta herramienta y evaluar cómo va variando el número de casos semana a semana.", unsafe_allow_html=False)
    adeno_desagrup = solo_ped.copy()
    adeno_desagrup['ESTUDIO'].replace(['ADENOVIRUS POR PCR', 'ADV: DETERMINACIÓN Y/O CARGA'], 'ADENOVIRUS', inplace=True)
    temp_df = adeno_desagrup.groupby(["ESTUDIO", "SEMANA_EPI", "RESULTADO"]).count().reset_index()
    temp_df = temp_df[["ESTUDIO", "SEMANA_EPI", "RESULTADO", "FECHA_REC"]]
    temp_df.rename(columns={"FECHA_REC": "Cantidad"}, inplace=True)
    temp_df['SEMANA_EPI'] = temp_df['SEMANA_EPI'].astype(str).str[-2:]
    temp_df_sum = temp_df.groupby(["ESTUDIO", "SEMANA_EPI"])["Cantidad"].sum().reset_index()
    temp_df = pd.merge(temp_df, temp_df_sum, on=["ESTUDIO", "SEMANA_EPI"], how="left")
    temp_df.rename(columns={"Cantidad_x": "Cantidad", "Cantidad_y": "Total Estudiados", "SEMANA_EPI": "Semana Epidemiológica", "ESTUDIO": "Estudio", "RESULTADO": "Resultado"}, inplace=True)
    temp_df["Porcentaje"] = round(temp_df["Cantidad"]/temp_df["Total Estudiados"]*100, 1)


    # DataFrame Interactivo 2
    gb = GridOptionsBuilder.from_dataframe(temp_df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()
    
    grid_response = AgGrid(
        temp_df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        download_filename = "distribucion_por_se.csv",
        download_button = "Descargar tabla",
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme='alpine', #Add theme color to the table
        enable_enterprise_modules=True,
        height=600, 
        width='100%',
        reload_data=True
    )
    
    # Crear un botón de descarga
    csv2 = temp_df.to_csv(index=False).encode()
    st.download_button(
        label=download_button,
        data=csv2,
        file_name="distribucion_por_se.csv",
        mime="text/csv",
    )
    
    data = grid_response['data']
    selected = grid_response['selected_rows'] 
    df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

    if selected:
        
        fig = px.bar(df, x="Semana Epidemiológica", y="Porcentaje", color="Resultado", color_discrete_map=color_dict, title="Porcentaje de Positividad por Semana Epidemiológica")
        fig.update_layout(xaxis=dict(tickmode="linear", tick0=1, dtick=1))
        st.plotly_chart(fig)
    # else:
    #     st.write("Seleccioná las filas de la tabla anterior presionando la tecla Shift del teclado y, simultáneamente, hacé click en el DataFrame interactivo para visualizar el Porcentaje de Positividad según la Semana Epidemiológica. No olvides filtrar 'No detectable' de la columna Resultado.")

    
    # Positivos por edad. Generar una tabla de positivos en la que las filas sean las categorías de edad y las columnas todos los virus.Filled area plot circulación de virus respiratorios por edad
    st.subheader("Distribución porcentual de los Virus Respiratorios por Categoría de Edad")
    st.caption("📌 En el siguiente gráfico de área se muestran los virus .", unsafe_allow_html=False)
    import plotly.graph_objects as go
    
    def chart_container() -> None:

        # Agrupar por categoría de edad y resultado y contar el número de pacientes
        solo_ped_positivos = solo_ped.loc[solo_ped['RESULTADO'] != 'No detectable']
        total_cat = solo_ped_positivos.groupby(['CAT_EDAD', 'RESULTADO']).size().reset_index(name='CANTIDAD')  
        # Calcular el total de pacientes por categoría de edad
        total_pacientes = total_cat.groupby(['CAT_EDAD'])['CANTIDAD'].transform('sum')    
        # Calcular el porcentaje de cada virus por categoría de edad
        total_cat['PORCENTAJE'] = 100 * total_cat['CANTIDAD'] / total_pacientes
        total_cat['PORCENTAJE'] = round(total_cat['PORCENTAJE'], 2)
        # Ordenar los resultados por categoría de edad y virus
        total_cat = total_cat.sort_values(['CAT_EDAD', 'RESULTADO'])
        total_cat_pivot = total_cat.pivot(index='CAT_EDAD', columns='RESULTADO', values='PORCENTAJE').fillna(0)
        # st.write(total_cat_pivot)
 
        # Seleccionar las columnas a quitar del gráfico
        selected_columns = st.multiselect(
            "Seleccione las columnas que desea quitar del gráfico de área:",
            total_cat_pivot.columns.tolist(),
            default=total_cat_pivot.columns.tolist(),
        )
        
        # Filtrar las columnas seleccionadas en el dataframe
        filtered_df = total_cat_pivot[selected_columns]
        
        # Creamos la figura de Plotly
        fig = px.area(filtered_df, x=filtered_df.index, y=filtered_df.columns, color_discrete_sequence=[color_dict[virus] for virus in filtered_df.columns])
        
        # Configuramos la figura y la mostramos en Streamlit
        fig.update_layout(
            title="Distribución de la circulación de Virus Respiratorios por Categoría de Edad",
            xaxis_title="Edad por Categoría",
            yaxis_title="Porcentaje",
            legend_title="Resultado",
            height=500,
            width=None
        )
        tabs = st.tabs(['Gráfico📈', 'Dataframe📄', 'Edades por Categorías📄', 'Descargar📁'])
        with tabs[0]:
            st.plotly_chart(fig)

        with tabs[1]:
            st.dataframe(filtered_df)

        with tabs[2]:
            # Tabla categorías de edad
            cat_edad = {
                      "Categoría de Edad": ["1", "2", "3", "4", "5", "6", "7"],
                      "Edad": ["< 6 meses", "6 a 12 meses", "> 12 a 23 meses", "2 a 4 años", "> 4 a 9 años", "> 9 a 14 años", "> 14 a 19 años"]
                      }
            cat_edad = pd.DataFrame(cat_edad)
            st.dataframe(cat_edad)
            
        with tabs[3]:
            st.download_button('Descargar tabla', data=export_csv(data), file_name='distribucion_virusresp.csv', mime='text/csv')
    
    
    if __name__ == '__main__':
        
        # Creamos el contenedor
        chart_container()
    
    
    # Coinfectados
    st.subheader("Análisis de Coinfecciones Virales")
    st.caption("📌  .", unsafe_allow_html=False)

    
    # inf_mixtas es un dataframe con todos los pacientes que aparecen más de una vez en positivos. Acá se pueden encontrar pacientes coinfectados (más de un virus encontrado en muestras tomadas el mismo día), pacientes repetidos (es decir, diferentes virus en diferentes muestras tomadas en diferentes días pero de un mismo paciente), e infecciones recurrentes (mismo virus, mismo paciente, diferente fecha de toma de muestra y obviamente diferente muestra)
    inf_mixtas = positivos[positivos.duplicated(subset=['PAC_ID'], keep=False)]
    inf_mixtas = inf_mixtas.sort_values(["PAC_ID"])
        
    # Sacarme de encima a los que vinieron el mismo dia y se procesaron dos veces para el mismo virus o con el mismo resultado (ejemplo: adeno pcr y adeno carga)
    inf_mixtas = inf_mixtas.drop_duplicates(subset=["PAC_ID", "FECHA_REC", "RESULTADO"])
            
    # Eliminar los pacientes que aparecen una sola vez, luego de eliminar los duplicados (no son coinfectados ni recurrentes)
    inf_mixtas = inf_mixtas[inf_mixtas.duplicated(subset=["PAC_ID"], keep=False)]
            
    # Sacar las líneas de pancorona cuando cuando pancorona y SARS-CoV-2 son positivos al mismo tiempo:
        #1:Dividir en 2 el df, por un lado los positivos para pancorona y por el otro los positivos para sars-cov-2
    filtro_pancorona = inf_mixtas[inf_mixtas["RESULTADO"] == "Pancoronavirus"].reset_index()
    filtro_covid = inf_mixtas[inf_mixtas["RESULTADO"] == "SARS-CoV-2"]
    #2:Generar la intersección entre esos dataframes en funcion de pac_id y fecha (para asegurarme que pancorona y sars dieron positivo en el mismo momento en el mismo paciente)
    intersection = filtro_covid[["PAC_ID", "FECHA_REC"]].merge(filtro_pancorona[["PAC_ID", "FECHA_REC"]])
    #3:Unir la intersección con los pancorona
    intersection = filtro_pancorona.merge(intersection).set_index("index")
    #4:Sacar los pancorona
    inf_mixtas.drop(intersection.index, inplace=True)    
    #5 Eliminar pacientes que aparecen una sola vez, luego de eliminar los pancorona
    inf_mixtas = inf_mixtas[inf_mixtas.duplicated(subset=["PAC_ID"], keep=False)]
    # st.dataframe(inf_mixtas)
        
    # Generar un dataframe solo con los coinfectados
    coinfectados = inf_mixtas[inf_mixtas.duplicated(subset=["NUMERO"], keep=False)]
    # st.write(coinfectados)
    # Contar coinfectados? metrica?
    
    
    st.markdown("")
    see_data = st.expander('Puede hacer click aquí para ver los datos crudos primero 👉')
    with see_data:
       st.dataframe(data=coinfectados.reset_index(drop=True))
    
    # Visualización de la cantidad de pacientes coinfectados por 2 virus o más
    coinf_cant = coinfectados.groupby(["PAC_ID", "FECHA_REC"]).size().to_frame()
    coinf_cant.rename(columns={0: "CANT"}, inplace=True)
    coinf_cant.reset_index(inplace=True)
        
    # Heatmap de coinfectados con 2 virus
    import numpy as np
    vector = coinf_cant[coinf_cant["CANT"] == 2]["PAC_ID"].unique()
    coinf_2virus = coinfectados.loc[coinfectados["PAC_ID"].isin(vector)]
    s = pd.crosstab(coinf_2virus.PAC_ID, coinf_2virus.RESULTADO)
    matriz_coinf = s.T.dot(s)
    np.fill_diagonal(matriz_coinf.values, matriz_coinf.values.diagonal() - s.sum())
        
    heatmap = px.imshow(matriz_coinf, color_continuous_scale='dense')
    st.plotly_chart(heatmap, height=1000, width=1000)
        
    # Pacientes coinfectados con más de 2 virus (no representados en el heatmap) ESTO DEBE SER UN CONDICIONAL PARA QUE NO APAREZCA UN DATAFRAME VACIO EN LA PAGINA!!!       
    # vector = coinf_cant[coinf_cant["CANT"] > 2]["PAC_ID"].unique()
    # multi_coinf = coinfectados.loc[coinfectados["PAC_ID"].isin(vector)]
    # st.dataframe(multi_coinf)
    
    
    # # Número de pacientes con más de un virus detectado en el período del tiempo consultado (independientemente si son de la misma muestra o diferente)
    # pac_multinfectados = len(inf_mixtas["PAC_ID"].unique())
    # st.write(pac_multinfectados)
    
    # # Porcentaje de pacientes con más de un virus detectado (independientemente si son de la misma muestra o no)
    # st.write(round(pac_multinfectados*100/len(solo_ped), 2))
    
    # # Infecciones recurrentes: pacientes que aparecen varias veces porque vinieron en diferentes oportunidades pero están infectados con el mismo virus
    # # Tener en cuenta: Dentro de infecciones recurrentes puede haber coinfectados
    # inf_recurrentes = inf_mixtas[inf_mixtas.duplicated(subset=["PAC_ID", "RESULTADO"], keep=False)]
    # pac_recurrentes = len(inf_recurrentes["PAC_ID"].unique())
    # st.write(pac_recurrentes)
    
    # # Porcentaje de pacientes con infecciones recurrentes
    # st.write(round(pac_recurrentes*100/len(solo_ped), 2))
    
    
    # # Vector en el que todo lo que es CANT > 1 es coinfección y todo lo que es CANT = 1 es infección recurrente
    # # Hay que restar los coinfectados de infecciones recurrentes
    # vector= inf_recurrentes.groupby(["PAC_ID", "NOMBRE_COMPLETO", "FECHA_REC"]).size().to_frame()
    # vector.rename(columns={0: "CANT"}, inplace=True)
    # vector.reset_index(inplace=True)
    # filtro_vector = vector[vector["CANT"] == 2].reset_index()
    

    
    # Infecciones Recurrentes
    
    # Blurear o *** los nombres de los pacientes para exponer en Streamlit
    
    # Averiguar cómo hacer para que no se pierdan los análisis cuando me muevo de página cuando uso el sidebar
        
    # Agregar análisis estadísticos: analizar si hay diferencias significativas en la misma semana entre los diferentes virus y además analizar si hay diferencias significativas entre semanas epidemiológicas siguiendo un mismo virus (estacionalidad de los virus respiratorios)
    
    
    
else:
    st.warning("Seleccione al menos un archivo .csv")
 



