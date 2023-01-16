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
st.subheader("¡Bienvenidos!")
st.caption("Esta aplicación fue desarrollada por el equipo de Bioinformática del Hospital de Pediatría S.A.M.I.C. 'Prof. Dr. Juan P. Garrahan'.")
st.caption("La fuente de información utilizada para el análisis de datos proviene del sistema informático hospitalario SIG-HG.")


