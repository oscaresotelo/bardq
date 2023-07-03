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
st.markdown(
    """
    <style>
        div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
        /* Estilos generales */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f1f1f1;
            margin: 0;
            padding: 0;
        }
        button.step-up {display: none;}
        button.step-down {display: none;}
        div[data-baseweb] {border-radius: 4px;}
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 4px;
        }
        
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Estilos del formulario */
        form {
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        .form-group input[type="text"],
        .form-group input[type="number"],
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        
        .form-group textarea {
            height: 100px;
            resize: vertical;
        }
        
        .form-submit-button {
            display: block;
            width: 100%;
            padding: 10px;
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .form-submit-button:hover {
            background-color: #0056b3;
        }
        
        .success-message {
            margin-top: 20px;
            padding: 10px;
            color: #155724;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
        }
        
        .error-message {
            margin-top: 20px;
            padding: 10px;
            color: #721c24;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuración de la API de Bard
os.environ['_BARD_API_KEY'] = "XQhlcrMY8LmPIMgZerlkEworuoOUVxaQYoRksshTR9zaFvt2VDYP1CCf92nPhr60JKKgJg."
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
def translate_to_english(text):
    blob = TextBlob(text)
    return str(blob.translate(from_lang="es", to='en'))

# Función para traducir texto al español
def translate_to_spanish(text):
    blob = TextBlob(text)
    return str(blob.translate(from_lang="en", to='es'))

# Función para obtener la respuesta de Bard
def prompt_bard(prompt):
    prompt_english = translate_to_english(prompt)
    response = bard.get_answer(prompt_english)['content']
    return response

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
    prompt_text = "necesito que actúes como un desarrollador experto en Streamlit, IMPORTANTE DEBES USAR LIBRERÍAS ACTUALIZADAS. IMPORTANTE DEBES CONTROLAR LA SINTAXIS DEL CÓDIGO GENERADO ANTES DE PRESENTARLO SI ESTÁ BIEN RECIÉN PRESENTAR. " + prompt_text + " Generar el código en un solo archivo y controlar la sintaxis antes de generarlo. El formulario debe estar en español."
    
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
