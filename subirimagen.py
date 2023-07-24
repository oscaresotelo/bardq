import streamlit as st
import cloudinary
import cloudinary.uploader
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from bardapi import Bard
import os 

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



# Configura tu cuenta de Cloudinary
cloudinary.config(
    cloud_name='dxe1nduh4',
    api_key='573436633192792',
    api_secret='5cA5vSrDNN_-q6xtqDijz5pYsrM'
)

GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwn-KjyS7S_bFAdbujXOmwebd8vdA1vXO539Ijr_RiC22gfVMDPkMYLcByjWrN1xXg/exec'
GOOGLE_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1Fa-B9CWSDsctbWFjcidB5GqY_3uk8ME5dxoaPBU0lbA/edit#gid=0'

def upload_image_to_cloudinary(image):
    try:
        response = cloudinary.uploader.upload(image)
        return response.get('secure_url', None)
    except Exception as e:
        st.error(f"Error al cargar la imagen en Cloudinary: {str(e)}")
        return None

def get_value_from_google_sheet(link):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(GOOGLE_SHEET_URL).get_worksheet(0)
    time.sleep(3)
    # Buscar el link en la columna "f" y obtener el valor de la columna "g" correspondiente
    cell = sheet.find(link)
    value = sheet.cell(cell.row, 7).value
    return value

def main():
    st.title("Ai-Cito")
    st.write("Sube una imagen ")
    if "textoext" not in st.session_state:
      st.session_state.textoext = ""
    uploaded_image = st.file_uploader("Selecciona una imagen", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.sidebar.image(uploaded_image, caption="Imagen subida", use_column_width=True)
        with st.spinner("Procesando......"):
            url = upload_image_to_cloudinary(uploaded_image)
            if url:
                # st.success("¡Imagen cargada correctamente")
                # st.image(url, caption="Imagen en Cloudinary", use_column_width=True)

                # Guardar la URL en la hoja de Google Sheets
                data = {
                    'func': 'Create',
                    'usuario': 'NombreUsuario',  # Reemplaza esto por el nombre del usuario
                    'comercio': 'NombreComercio',  # Reemplaza esto por el nombre del comercio
                    'provincia': 'NombreProvincia',  # Reemplaza esto por el nombre de la provincia
                    'fecha': 'FechaActual',  # Reemplaza esto por la fecha actual (por ejemplo, "2023-07-24")
                    'link': url,
                    'observacion': 'Observacion'  # Reemplaza esto con una observación opcional
                }

                response = requests.post(GOOGLE_SCRIPT_URL, data=data)
                # if response.status_code == 200:
                #     st.success("Cargada Correctamente.")

                # else:
                #     st.error("Error al leer imagen")
                    
                # Obtener el valor de la columna "g" de la hoja de Google Sheets
                value_from_sheet = get_value_from_google_sheet(url)
                st.session_state.textoext = value_from_sheet
                # st.text_area("Texto Extraido" ,value_from_sheet, height= 400)

            else:
    
                st.error("Error al cargar la imagen ")
    texto_extraido = st.text_area("Texto Extraido", st.session_state.textoext, height = 400)
    boton_ask= st.button("Procesar Respuesta") 
    if boton_ask:
      pregunta = texto_extraido
      bard = Bard(timeout=30, session=session)  # Set timeout in seconds
      result = bard.get_answer(pregunta)['content']
      st.write(result)        

if __name__ == "__main__":
    main()
