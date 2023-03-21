# Análisis de datos epidemiológicos de Infecciones Respiratorias Agudas Virales (IRAV)
Esta aplicación es una herramienta diseñada para analizar datos epidemiológicos sobre Infecciones Respiratorias Agudas Virales (IRAV). Su interfaz interactiva permite a los usuarios cargar y visualizar datos de manera fácil y rápida.

## ¿Qué hace la aplicación?
Utilizando técnicas de análisis de datos avanzadas, la aplicación transforma esta información en conocimientos valiosos sobre la propagación de las enfermedades respiratorias y su impacto en la salud pública pediátrica. Los usuarios pueden interactuar con la aplicación para explorar diferentes conjuntos de datos, comparar estadísticas y visualizar gráficos. Además, estas herramientas de visualización permiten a los usuarios identificar patrones y tendencias en los datos.

## ¿Cómo utilizar la aplicación?
Existen dos alternativas para utilizar esta aplicación: de manera local y online.


Para utilizar la aplicación de forma **local**, siga los siguientes pasos:

### Clone el repositorio
1. Abra la página del repositorio en GitHub.
2. Haga click en el botón "Code" y seleccione "Download ZIP" para descargar el repositorio como un archivo comprimido ZIP.
3. Extraiga el archivo ZIP en una carpeta de su elección.

### Instale las dependencias
4. Abra una terminal y navegue hasta la carpeta del repositorio clonado.
5. Cree un entorno virtual de Python:
      - En Windows: python -m venv venv
      - En Linux/Mac: python3 -m venv venv
6. Active el entorno virtual:
      - En Windows: venv\Scripts\activate.bat
      - En Linux/Mac: source venv/bin/activate
7. Instale las dependencias:

```
pip install -r requirements.txt
```


### Ejecute la aplicación
8. Ejecute el siguiente comando para iniciar la aplicación:
      

```
streamlit run Home.py
```
            
            
9. La aplicación se ejecutará en su navegador predeterminado. Si no se abre automáticamente, puede acceder a ella en su navegador visitando http://localhost:8501.        


Para utilizar la aplicación de forma **online**, simplemente siga estos pasos:

  1. Ingrese al link: https://lauridangut-boletin-epidemio-docshome-9kbf0q.streamlit.app/
  2. Diríjase a la página de análisis en la barra lateral.
  3. Seleccione el conjunto de datos que desea cargar.
  4. Interactúe con la aplicación para explorar los datos, comparar estadísticas y visualizar gráficos.
  5. Descargue gráficos y tablas.
  6. Guarde un reporte de sus análisis en formato pdf haciendo click en el menú hamburguesa del extremo superior derecho de la aplicación y luego en "Print". Posteriormente seleccione la opción "Save as PDF".

## Requerimientos
Para utilizar la aplicación de forma local es necesario tener instalado lo siguiente:

  - Python 3.7 o superior.
  - Las bibliotecas de Python especificadas en requirements.txt.

## Agradecimientos
Esta aplicación fue desarrollada por Laura Gutiérrez y supervisada por Martín Ruhle, en el marco de una Beca de Bioinformática Aplicada a la Virología Clínica. Agradecemos al laboratorio de Bioinformática y al Servicio de Microbiología del Hospital que nos apoyaron en su desarrollo.

## Contacto
Si tiene alguna pregunta o sugerencia, no dude en contactarnos en laura.d.gutierrez@alumni.garrahan.edu.ar. ¡Gracias por utilizar nuestra aplicación!

