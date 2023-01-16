#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 14:10:22 2023

@author: usuario
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
import datetime


#Título de la página
st.set_page_config(page_title='Aplicación para la vigilancia epidemiológica de los Virus Respiratorios.',page_icon="/home/usuario/Downloads/Laura/boletin_epidemio/img/virus.png", layout="wide")

# Add social media tags and links to the web page.

# [![Star](https://www.garrahan.gov.ar/home-intranet/intranet-prensa/noticias-internas/)
"""
# Servicio de Microbiología - Hospital de Pediatría S.A.M.I.C. "Prof. Dr. Juan P. Garrahan"

"""

# Add a sidebar to the web page.
st.markdown('---')
# Sidebar Configuration
st.sidebar.image(
    '/home/usuario/Downloads/Laura/boletin_epidemio/img/logo_garrahan.png', width=200)
st.sidebar.markdown('# Unidad de Virología y Epidemiología Molecular')
st.sidebar.markdown('El equipo de Bioinformática desarrolla el análisis de los casos estudiados por la Unidad de Virología y Epidemiología Molecular para la detección de virus respiratorios bajo vigilancia en nuestro país.')
st.sidebar.markdown(
    'El objetivo del mismo es reconocer la situación actual de estos eventos en la población que concurre al hospital y contribuir, de esta forma, con la toma de decisiones.')
st.sidebar.markdown(
    'La fuente de información utilizada para la elaboración de este análisis son los datos extraídos del sistema informático hospitalario SIG-HG.')

st.sidebar.markdown('---')
st.sidebar.write('Contacto: laura.d.gutierrez@alumni.garrahan.edu.ar')
