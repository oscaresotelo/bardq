# import streamlit as st
# from Bard import Chatbot

# # Paste your Bard Token (check README.md for where to find yours) 
# token = "Wghlci3JMlUaLO4_VZgMKjCDDhUSMRvL4049frEMZZaj3PK1cJ6iMDTJbZoeClmdcGaRYg."
# # Initialize Google Bard API
# chatbot = Chatbot(token)

# def prompt_bard(prompt):
#     response = chatbot.ask(prompt)
#     return response['content']

# def main():
#     st.title("Preguntame")
#     st.write("Ingrese sus Preguntas")

#     prompt_text = st.text_input("Pregunta")
#     if st.button("Preguntar"):
#         # If prompt is empty, show error message
#         if len(prompt_text.strip()) == 0:
#             st.error("Por Favor Ingresar Pregunta")
#         else:
#             # Prompt Bard
#             response = prompt_bard(prompt_text)
#             st.write('Respuesta:', response)

# if __name__ == '__main__':
#     main()
import streamlit as st
from translate import Translator

from Bard import Chatbot

# Pegue su token de Bard (consulte el archivo README.md para saber dónde encontrar el suyo)
token = "Wghlci3JMlUaLO4_VZgMKjCDDhUSMRvL4049frEMZZaj3PK1cJ6iMDTJbZoeClmdcGaRYg."
# Inicializar el Chatbot de Bard
chatbot = Chatbot(token)

# Inicializar el traductor
def translate_to_spanish(text):
    translator = Translator(to_lang="es", from_lang="en")
    translation = translator.translate(text)
    return translation

def translate_to_english(text):
    translator = Translator(to_lang="en", from_lang="es")
    translation = translator.translate(text)
    return translation

def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']

def split_into_segments(text, segment_length):
    segments = []
    for i in range(0, len(text), segment_length):
        segment = text[i:i + segment_length]
        segments.append(segment)
    return segments

def main():
    st.title("Pregúntame")
    st.write("Ingrese sus Preguntas")

    prompt_text = st.text_input("Pregunta")
    if st.button("Preguntar"):
        # Si la pregunta está vacía, mostrar mensaje de error
        if len(prompt_text.strip()) == 0:
            st.error("Por favor ingrese una pregunta")
        else:
            # Preguntar a Bard
            prompt_text = translate_to_english(prompt_text)
            response = prompt_bard(prompt_text)
            segments = split_into_segments(response, 400)
            translated_segments = [translate_to_spanish(segment) for segment in segments]
            translated_response = ''.join(translated_segments)
            st.write('Respuesta:', translated_response)

if __name__ == '__main__':
    main()
