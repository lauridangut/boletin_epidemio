#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:21:50 2023

@author: usuario
"""
import streamlit as st
import pdfkit


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
        
descripcion = "Descargue los análisis realizados en formato PDF"
        
colored_header(
    label="Reporte del Análisis Epidemiológico",
    description=descripcion,
    color_name="#9d4edd",
)


def streamlit_to_pdf(filename):
    config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm'
    }
    pdfkit.from_file(filename, 'report.pdf', configuration=config, options=options)

if st.button('Generar reporte en PDF'):
    streamlit_to_pdf('3_Información_Destacada.py')
    st.success('¡El reporte en PDF ha sido generado con éxito!')
