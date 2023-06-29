import streamlit as st
from Bard import Chatbot
from textblob import TextBlob
import warnings
import sys
from bardapi import Bard
import os
import requests
import re
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
def translate_to_english(text):
    blob = TextBlob(text)
    return str(blob.translate(from_lang= "es",to='en'))

def translate_to_spanish(text):
    blob = TextBlob(text)
    return str(blob.translate(from_lang="en",to='es'))

def prompt_bard(prompt):
    prompt_english = translate_to_english(prompt)
    response = bard.get_answer(prompt_english)['content']
    
    # response_spanish = translate_to_spanish(response)
    # return response_spanish
    return response
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
pregunta = """ necesito que actues como un desarrollador experto en streamlit, debes usar librerias actualizadas, IMPORTANTE
DEBES CONTROLAR LA SINTAXIS DEL CODIGO GENERADO, el pedido es el siguiente:   """
final = """ generar el codigo en uns solo archivo, y controlar la sintaxis antes de generarlo,el formulario debe estar en español"""

def main():
    st.title("Generador de Soluciones")
    if "codigo" not in st.session_state:
        st.session_state.codigo = ""
    prompt_text = st.text_area("Escribir Solicitud:")
    prompt_text = pregunta + prompt_text + final
    if st.button("Preguntar"):
        with st.spinner('Procesando Solicitud, Tardara Unos Segundos...'):
            if len(prompt_text.strip()) == 0:
                st.warning("Vacio, Pregunte Nuevamente.")
            else:
                response = prompt_bard(prompt_text)
                st.session_state.codigo = (extract_python_code(prompt_bard(prompt_text)))
                # exec(st.session_state.codigo, globals())
                # st.text_area(response)
    exec(st.session_state.codigo, globals())
if __name__ == "__main__":
    main()

