from bardapi import Bard
import os


os.environ['_BARD_API_KEY'] = "awhlcqUB-BzFJrSuhTJw7teBxj0J21mqlVL8KGVEDCecyXHJCXGjLtnyBJaUlBSdvAzY6w."


print(Bard().get_answer("import streamlit as st, crear formulario para dar de alta empleados")['content'])
