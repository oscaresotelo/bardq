
from bardapi import Bard
import streamlit as st
from gtts import gTTS
import tempfile
import os
token = 'YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ.'
bard = Bard(token=token)

def text_to_speech(text):
	
	tts = gTTS(text=text, lang="es", tld='us')
	temp_file = tempfile.NamedTemporaryFile(delete=False)
	temp_file.close()
	tts.save(temp_file.name)
	return temp_file.name

def main():
    st.title("Ai - Cito")
    opcion = st.radio("Selecciona una opción:", ("Resolver Cuestionario", "Generar Resumen"))
    uploaded_image = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image_data = uploaded_image.read()  # Read the uploaded image as bytes
        
        st.sidebar.image(uploaded_image, caption="Imagen subida", use_column_width=True)
        
        if opcion == "cuestionario":
            with st.spinner("Procesando..."):
                bard_answer = bard.ask_about_image("answer the questions in spanish", image_data)
                st.write(bard_answer['content'])
        else:
            with st.spinner("Procesando..."):
                bard_answer = bard.ask_about_image("summarize the text in spanish", image_data)
                respuesta = bard_answer['content']
                st.write(respuesta)
                # audio_file = bard.speech(respuesta)
                audio_file = text_to_speech(respuesta)
                st.audio(audio_file, format='audio/mp3')
                os.remove(audio_file)
if __name__ == "__main__":
    main()
