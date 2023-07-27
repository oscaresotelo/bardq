import streamlit as st
import cloudinary
import cloudinary.uploader
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from bardapi import Bard
import os 
import base64

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

@st.cache_data
def upload_image_to_cloudinary(image):
    try:
        response = cloudinary.uploader.upload(image)
        return response.get('secure_url', None)
    except Exception as e:
        st.error(f"Error al cargar la imagen en Cloudinary: {str(e)}")
        return None
@st.cache_data
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
expander = st.expander("Instrucciones:")
expander.write(""" Debe subir una imagen, al hacerlo se visualizara la misma en el panel derecho,
  el texto extraido de la misma se reflejara en pantalla , editar el texto de la misma para obtener un resultado
  satisfactorio, en la parte superior del texto debe escribir las instrucciones de lo que desea realizar, por ejemplo
  resumir el siguiente texto, resolver las siguientes operaciones, contestar el siguiente cuestionario, etc.
  Presionar el boton  'Procesar respuesta' para obtener lo solicitado """)
def main():
    
    
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
     
    # if boton_ask:
    #   pregunta = texto_extraido
    #   bard = Bard(timeout=30, session=session)  # Set timeout in seconds
    #   result = bard.get_answer(pregunta)['content']
    #   st.write(result)        

if __name__ == "__main__":
    main()
boton_ask= st.button("Procesar Respuesta")
if boton_ask:
      # pregunta = texto_extraido
      bard = Bard(timeout=30, session=session)  # Set timeout in seconds
      result = bard.get_answer(st.session_state.textoext)['content']
      st.write(result)   