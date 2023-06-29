import streamlit as st
from Bard import Chatbot
from textblob import TextBlob

import warnings
import sys

# Paste your Bard Token (check README.md for where to find yours) 
token = "XQhlcrMY8LmPIMgZerlkEworuoOUVxaQYoRksshTR9zaFvt2VDYP1CCf92nPhr60JKKgJg."
# Initialize Google Bard API
chatbot = Chatbot(token)

def translate_to_english(text):
    blob = TextBlob(text)
    return str(blob.translate(from_lang= "es",to='en'))

def translate_to_spanish(text):
    blob = TextBlob(text)
    return str(blob.translate(from_lang="en",to='es'))

def prompt_bard(prompt):
    prompt_english = translate_to_english(prompt)
    response = chatbot.ask(prompt_english)
    response_spanish = translate_to_spanish(response['content'])
    return response_spanish

def main():
    st.title("Pregúntame")
    prompt_text = st.text_input("Escribir:")
    if st.button("Preguntar"):
        if len(prompt_text.strip()) == 0:
            st.warning("Vacio, Pregunte Nuevamente.")
        else:
            response = prompt_bard(prompt_text)
            
            st.write(response)

if __name__ == "__main__":
    main()

