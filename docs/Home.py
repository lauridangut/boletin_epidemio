#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 14:10:22 2023

@author: usuario
"""
import streamlit as st

#Título de la página
st.set_page_config(
    page_title="Aplicación para la vigilancia epidemiológica de los Virus Respiratorios",
    page_icon="https://raw.githubusercontent.com/lauridangut/boletin_epidemio/main/img/virus.png", 
    layout="wide"
    )

#Barra lateral
st.sidebar.markdown('# Unidad de Virología y Epidemiología Molecular')
st.sidebar.image(
    'https://raw.githubusercontent.com/lauridangut/boletin_epidemio/demo/img/logo_transparente.png', width=200)

#Principal
st.header("Servicio de Microbiología - Hospital de Pediatría S.A.M.I.C. 'Prof. Dr. Juan P. Garrahan'")

#Cuerpo
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
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px; text-align: justify">',
        unsafe_allow_html=True,
    )
    if description:
        st.write(description)


titulo = "¡Bienvenidos!"
descripcion = "Esta aplicación es una herramienta diseñada para analizar datos epidemiológicos sobre Infecciones Respiratorias Agudas Virales. Su interfaz interactiva permite a los usuarios cargar y visualizar datos de manera fácil y rápida. Utilizando técnicas de análisis de datos avanzadas, la aplicación transforma esta información en conocimientos valiosos sobre la propagación de las enfermedades respiratorias y su impacto en la salud pública pediátrica. Los usuarios pueden interactuar con la aplicación para explorar diferentes conjuntos de datos, comparar estadísticas y visualizar gráficos. Además, estas herramientas de visualización permiten a los usuarios identificar patrones y tendencias en los datos. Con esta información, los profesionales de la salud y los investigadores pueden tomar decisiones informadas en lo concerniente a las Infecciones Respiratorias Agudas Virales en pos de la salud pública pediátrica."
colored_header(
    label=titulo,
    description=descripcion,
    color_name="#9d4edd",
)
