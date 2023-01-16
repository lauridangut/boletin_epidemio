#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:38:56 2023

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
st.caption("El objetivo de esta aplicación es facilitar la visualización y el análisis de los datos que resultan del procesamiento de las muestras respiratorias de pacientes que concurren a nuestro hospital, de manera que sea posible reconocer la situación actual de los eventos bajo Vigilancia Epidemiológica y contribuir, de esta forma, con la toma de decisiones.")

