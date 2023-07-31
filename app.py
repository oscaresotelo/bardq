from bardapi import Bard
import os


os.environ['_BARD_API_KEY'] = "ZQhlchn_uUBoRxKJBFeft1KPTy312zCh1V4TI5jEq0Gk3lTO1Z0SRNBKTLspZUhE69r1dA."


print(Bard().get_answer("import streamlit as st, crear formulario para dar de alta empleados")['content'])