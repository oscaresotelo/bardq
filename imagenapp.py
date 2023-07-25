
from bardapi import Bard
import streamlit as st

token = 'YwhlcoKaK4On2dndWfbCoX9MifhxeC_5mVs6d6WAHBlGs3J88otYTjI0NKeHYH4R90VSrQ.'
bard = Bard(token=token)

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
                st.write(bard_answer['content'])

if __name__ == "__main__":
    main()
