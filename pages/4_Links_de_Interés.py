#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:22:04 2023

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
        
descripcion = ""
        
colored_header(
    label="Links de interés",
    description=descripcion,
    color_name="#9d4edd",
)

# Intranet Hospital Garrahan
link = '<a href="https://www.garrahan.gov.ar/home-intranet/intranet-prensa/noticias-internas/">Intranet del Hospital Garrahan</a>'
st.write(link, unsafe_allow_html=True)

# Web Ministerio de Salud
link = '<a href="https://www.argentina.gob.ar/salud/coronavirus-COVID-19?utm_source=search&utm_medium=cpc&utm_campaign=coronavirus&utm_term=grants&utm_content=nacional&gclid=Cj0KCQiA0oagBhDHARIsAI-BbgdPD9t2kjf9f64msNcNQy0Z_2Fg0szTrt-gAzrtOgiejZXid4-M7HYaAtPyEALw_wcB">Ministerio de Salud de la Nación</a>'
st.write(link, unsafe_allow_html=True)

# Web OPS
link = '<a href="https://www.paho.org/es">Organización Panamericana de la Salud</a>'
st.write(link, unsafe_allow_html=True)

# Web OMS
link = '<a href="https://www.who.int/es">Organización Mundial de la Salud</a>'
st.write(link, unsafe_allow_html=True)

# Sociedad Argentina de Pediatría
link = '<a href="https://www.sap.org.ar/">Sociedad Argentina de Pediatría</a>'
st.write(link, unsafe_allow_html=True)

# Asociación Argentina de Microbiología
link = '<a href="https://www.aam.org.ar/">Asociación Argentina de Microbiología</a>'
st.write(link, unsafe_allow_html=True)

# ViralZone
link = '<a href="https://viralzone.expasy.org/">Viral Zone</a>'
st.write(link, unsafe_allow_html=True)

# Web Pubmed
link = '<a href="https://pubmed.ncbi.nlm.nih.gov/">PubMed</a>'
st.write(link, unsafe_allow_html=True)

# Calendario Epidemiológico 2022
link = '<a href="https://bancos.salud.gob.ar/recurso/calendario-epidemiologico-2022">Calendario Epidemiológico 2022</a>'
st.write(link, unsafe_allow_html=True)

# Calendario Epidemiológico 2023
link = '<a href="https://bancos.salud.gob.ar/recurso/calendario-epidemiologico-2023">Calendario Epidemiológico 2023</a>'
st.write(link, unsafe_allow_html=True)