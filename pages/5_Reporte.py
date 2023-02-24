#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 15:21:50 2023

@author: usuario
"""
import streamlit as st
import pdfkit

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
