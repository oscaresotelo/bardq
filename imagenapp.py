
from bardapi import Bard
import streamlit as st
from gtts import gTTS
import tempfile
import os
import re
import base64

# Initialize Bard and Streamlit app
token = 'ZQhlchn_uUBoRxKJBFeft1KPTy312zCh1V4TI5jEq0Gk3lTO1Z0SRNBKTLspZUhE69r1dA.'
bard = Bard(token=token)


LOGO_IMAGE = "./imagenes/libros.jpg"
LOGO_IMAGE2 = "./imagenes/nino.jpg"

st.markdown(
    """
    <style>
        .container {
        display: flex;
    }
    .logo-img {
        max-width: 200px; /* Adjust the width to your desired value */
        max-height: 100px; /* Adjust the height to your desired value */
    }
    .logo-text {
        font-weight: 700 !important;
        font-size: 30px !important;
        color: gray !important;
        padding-top: 10px !important;
    }
    
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
            max-width: 400px;
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
        .container {
        display: flex;
    
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.markdown("<h1 style='color: gray; font-size: 60px;text-align: center;'>Ai-Cito</h1>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">Ai-Cito</p>
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE2, "rb").read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True
)
# st.title("Ai - Cito")


def extracter_texto(text):
   
    if "```python" in text:
        pattern = r"```python(.*?)```"
    else:
        pattern = r"```(.*?)```"
        
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return ""

# Function to convert text to speech
@st.cache_data
def text_to_speech(text):
    tts = gTTS(text=text, lang="es", tld='us')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

# Function to ask questions about the image
@st.cache_data
def ask_about_image(image_data):
    return bard.ask_about_image("answers the question or problems in the image,you migth speak in spanish, unless the text is in english", image_data)['content']

# Function to extract text from the image
@st.cache_data
def extract_text_from_image(image_data):
    
    return bard.ask_about_image("do not explain anything,do not translate to english , you migth speak in spanish,extract only text,  respecting the format, yoy migth speak in spanish", image_data)['content']

# Main app

opcion = st.radio("Selecciona una opción:", ("Resolver Cuestionario", "Editar Texto de Imagen para Procesar"))
uploaded_image = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image_data = uploaded_image.read()  # Read the uploaded image as bytes
    st.sidebar.image(uploaded_image, caption="Imagen subida", use_column_width=True)
    
    if opcion == "Resolver Cuestionario":
        with st.spinner("Procesando..."):
            respuesta = ask_about_image(image_data)
            st.write(respuesta)
            audio_file = text_to_speech(respuesta)
            st.audio(audio_file, format='audio/mp3')
            os.remove(audio_file)

    else:
        if opcion == "Editar Texto de Imagen para Procesar":
            if "texto" not in st.session_state:
                st.session_state.texto = ""
            with st.spinner("Procesando..."):
                respuesta = extract_text_from_image(image_data)
                # st.write(respuesta)
                # respuesta = extracter_texto(respuesta)
                st.session_state.texto = st.text_area("Respuesta", respuesta, height = 400)

    # Button to process the answer
boton_ask = st.button("Procesar Respuesta")
if boton_ask:

    result = bard.get_answer(st.session_state.texto)['content']

    st.write(result)
