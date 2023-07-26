
# from bardapi import Bard
# import streamlit as st
# from gtts import gTTS
# import tempfile
# import os
# token = 'YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ.'
# bard = Bard(token=token)

# def text_to_speech(text):
	
# 	tts = gTTS(text=text, lang="es", tld='us')
# 	temp_file = tempfile.NamedTemporaryFile(delete=False)
# 	temp_file.close()
# 	tts.save(temp_file.name)
# 	return temp_file.name


# st.title("Ai - Cito")

# opcion = st.radio("Selecciona una opción:", ("Resolver Cuestionario", "Generar Resumen"))
# uploaded_image = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

# if uploaded_image is not None:
#     image_data = uploaded_image.read()  # Read the uploaded image as bytes
        
#     st.sidebar.image(uploaded_image, caption="Imagen subida", use_column_width=True)
        
#     if opcion == "Resolver Cuestionario":
#         with st.spinner("Procesando..."):
#             bard_answer = bard.ask_about_image("answer the questions in spanish", image_data)
#             st.write(bard_answer['content'])
#             respuesta = bard_answer['content']
#             audio_file = text_to_speech(respuesta)
#             st.audio(audio_file, format='audio/mp3')
#             os.remove(audio_file)
                
#     else:
#         if "texto" not in st.session_state:
#             st.session_state.texto = ""
#         with st.spinner("Procesando..."):
#             bard_answer = bard.ask_about_image("extract only text, respecting the format", image_data)
#             respuesta = bard_answer['content']
#             st.session_state.texto = st.text_area("Respuesta",respuesta)
   


# boton_ask= st.button("Procesar Respuesta") 
# if boton_ask:
# 					# pregunta = texto_extraido
#         # bard = Bard(timeout=30, session=session)  # Set timeout in seconds
#     result = bard.get_answer(st.session_state.texto)['content']
#     st.write(result)  
#                 # audio_file = bard.speech(respuesta)
#                 
from bardapi import Bard
import streamlit as st
from gtts import gTTS
import tempfile
import os

# Initialize Bard and Streamlit app
token = 'YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ.'
bard = Bard(token=token)
st.title("Ai - Cito")

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
    return bard.ask_about_image("answer the questions in spanish", image_data)['content']

# Function to extract text from the image
@st.cache_data
def extract_text_from_image(image_data):
    return bard.ask_about_image("extract only text, respecting the format, all the text must be in spanish", image_data)['content']

# Main app
opcion = st.radio("Selecciona una opción:", ("Resolver Cuestionario", "Generar Resumen"))
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
        if "texto" not in st.session_state:
            st.session_state.texto = ""
        with st.spinner("Procesando..."):
            respuesta = extract_text_from_image(image_data)
            st.session_state.texto = st.text_area("Respuesta", respuesta)

    # Button to process the answer
boton_ask = st.button("Procesar Respuesta")
if boton_ask:
    result = bard.get_answer(st.session_state.texto)['content']
    st.write(result)
