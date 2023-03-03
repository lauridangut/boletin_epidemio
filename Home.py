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
    page_icon="/home/usuario/Downloads/Laura/boletin_epidemio/img/virus.png", 
    layout="wide"
    )

#Barra lateral
st.sidebar.markdown('# Unidad de Virología y Epidemiología Molecular')
st.sidebar.image(
    '/home/usuario/Downloads/Laura/boletin_epidemio/img/logo_garrahan.png', width=200)

#Principal
st.header("Servicio de Microbiología - Hospital de Pediatría S.A.M.I.C. 'Prof. Dr. Juan P. Garrahan'")

#Cuerpo
# st.subheader("¡Bienvenidos!")
# st.caption("Esta aplicación fue desarrollada por el equipo de Bioinformática del Hospital de Pediatría S.A.M.I.C. 'Prof. Dr. Juan P. Garrahan'.")
# st.caption("La fuente de información utilizada para el análisis de datos proviene del sistema informático hospitalario SIG-HG.")

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


titulo = "¡Bienvenidos!"
descripcion = "Esta es una aplicación que tiene como objetivo proporcionar una herramienta para analizar datos epidemiológicos sobre infecciones respiratorias producidas por virus. La misma es una interfaz de usuario interactiva que permite a los usuarios cargar y visualizar datos, así como aplicar técnicas de análisis de datos para obtener información relevante sobre la propagación de las enfermedades respiratorias y su impacto en la salud pública pediátrica."
colored_header(
    label=titulo,
    description=descripcion,
    color_name="#9d4edd",
)
