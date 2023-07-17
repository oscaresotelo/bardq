import streamlit as st
import sqlite3

from Bard import Chatbot
from textblob import TextBlob
import warnings
import sys
from bardapi import Bard
import os
import requests
import re
from st_pages import Page, show_pages, add_page_title
# Crear la conexión a la base de datos
conn = sqlite3.connect('codigopython.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS codigo
             (nombre TEXT, scriptcodigo TEXT)''')

# Clase personalizada para manejar el estado de la sesión
class SessionState:
    def __init__(self):
        self.codigo = ""

# Obtener el estado de la sesión o crear uno nuevo si no existe
def get_session_state():
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()
    return st.session_state.session_state

# Función para guardar el código en la base de datos
def guardar_codigo(nombre, codigo):
    c.execute("INSERT INTO codigo (nombre, scriptcodigo) VALUES (?, ?)", (nombre, codigo))
    conn.commit()


# Configuración de Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Configuración de la API de Bard
os.environ['_BARD_API_KEY'] = "YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ."
session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY"))
bard = Bard(timeout=30, session=session)

# Función para traducir texto al inglés
# def translate_to_english(text):
#     blob = TextBlob(text)
#     return str(blob.translate(from_lang="es", to='en'))

# # Función para traducir texto al español
# def translate_to_spanish(text):
#     blob = TextBlob(text)
#     return str(blob.translate(from_lang="en", to='es'))

# Función para obtener la respuesta de Bard
def prompt_bard(prompt):

    # prompt_english = translate_to_english(prompt)
    response = bard.get_answer(prompt)['content']
    return(response)

# Función para extraer el código Python de un texto
def extract_python_code(text):
   
    if "```python" in text:
        pattern = r"```python(.*?)```"
    else:
        pattern = r"```(.*?)```"
        
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return ""
show_pages([
        Page("guardacodigo.py", "Inicio", "🏠"),
        Page("ejectuarcodigo.py", "Soluciones Creadas", ":notebook:"),
    ])
# Interfaz principal de Streamlit
def main():
    st.title("Generador de Soluciones Administrativas")
    st.sidebar.title("Guardar Aplicacion")
    # Obtener el estado de la sesión
    session_state = get_session_state()
    
    # Campo de entrada de texto para el nombre
    nombre = st.sidebar.text_input("Nombre de la Aplicacion:")
    
    # Botón para guardar el código
    if st.sidebar.button("Guardar Aplicacion"):
        with st.spinner('Guardando Código en la Base de Datos...'):
            if len(session_state.codigo.strip()) == 0:
                st.warning("El código está vacío. No se guardará nada.")
            elif len(nombre.strip()) == 0:
                st.warning("Por favor, ingrese un nombre para el código.")
            else:
                guardar_codigo(nombre, session_state.codigo)
                st.success("Código guardado exitosamente en la base de datos.")
    
    prompt_text = st.text_area("Escribir Solicitud:")
    # prompt_text = "necesito que actúes como un desarrollador experto en Streamlit, IMPORTANTE DEBES USAR LIBRERÍAS ACTUALIZADAS,. IMPORTANTE DEBES CONTROLAR LA SINTAXIS DEL CÓDIGO GENERADO ANTES DE PRESENTARLO SI ESTÁ BIEN RECIÉN PRESENTAR. IMPORTANTE DEBES USAR LIBRERIAS ACTUALIZADAS, USAR PANDAS para TRABAJAR CON DATOS , controlar que no genere el siguiente error ' If using all scalar values, you must pass an index', USAR dataframe  PARA MOSTRAR DATOS, usar indices cuando sea necesario, el pedido es el siguiente:  " + prompt_text + " Generar el código en un solo archivo y controlar la sintaxis antes de generarlo. El formulario debe estar en español."
    consulta = """
            import streamlit as st,
            es obligatorio que este esta linea "import io",
            IMPORTANTE EL MANEJO DE DATOS SE HARA CON la biblioteca pandas
            IMPORTANTE PARA TRABAJAR CON ARCHIVOS EXCEL USARAS la biblioteca openpyxl,

            IMPORTANTE VERIFICAR QUE BIBLIOTECAS  NECESARIAS E IMPORTAR LAS BIBLIOTECAS NECESARIAS PARA QUE EL CODIGO SEA UTIL,
            
            usar loc para agregar nuevo registro en el caso que se use pandas,
            para usar crear formulario tener en cuenta la siguiente explicacion:

            "Create a form that batches elements together with a "Submit" button.

            A form is a container that visually groups other elements and widgets together, and contains a Submit button. When the form's Submit button is pressed, all widget values inside the form will be sent to Streamlit in a batch.

            To add elements to a form object, you can use "with" notation (preferred) or just call methods directly on the form. See examples below.

            Forms have a few constraints:

            Every form must contain a st.form_submit_button.
            st.button and st.download_button cannot be added to a form.
            Forms can appear anywhere in your app (sidebar, columns, etc), but they cannot be embedded inside other forms."

            IMPORTANTE LOS DATOS que se carguen , GUARDARLOS EN DICCIONARIOS USANDO session_state
            IMPORTANTE RECUERDA LO SIGUIENTE TAMBIEN "Para guardar un DataFrame de pandas en un archivo de Excel, puedes usar el método to_excel() de pandas."
            IMPORTANTE: IMPORTAR LAS LIBRERIAS NECESARIAS PARA QUE EL CODIGO SE UTIL, CONTROLAR ANTES DE GENERAR EL CODIGO
            escribir codigo de la siguiente pregunta:

           
            """
    prompt_text = consulta + prompt_text        
    if st.button("Generar"):
        with st.spinner('Procesando Solicitud, Tardará Unos Segundos...'):
            if len(prompt_text.strip()) == 0:
                st.warning("El campo de solicitud está vacío. Por favor, pregunte nuevamente.")
            else:
                response = prompt_bard(prompt_text)
                
               
                session_state.codigo = extract_python_code(response)
                
    exec(session_state.codigo, globals())

if __name__ == "__main__":
    main()
