import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title
# Conectarse a la base de datos SQLite
conn = sqlite3.connect('codigopython.db')
c = conn.cursor()

# Obtener todos los registros de la tabla 'codigo'
c.execute("SELECT nombre, scriptcodigo FROM codigo")
registros = c.fetchall()
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# Crear un botón para cada registro en la tabla
st.sidebar.title("Sistemas")


if "codigo" not in st.session_state:
            st.session_state.codigo = ""
for registro in registros:
    nombre = registro[0]
    script = registro[1]

    # Definir la función a ejecutar al hacer clic en el botón
    def ejecutar_codigo(script=script):
        
        st.session_state.codigo = script
        
    
    # Agregar el botón a la aplicación Streamlit

    st.sidebar.button(nombre, on_click=ejecutar_codigo)
exec(st.session_state.codigo, globals())

# Cerrar la conexión a la base de datos SQLite
conn.close()
