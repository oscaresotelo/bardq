
from bardapi import Bard
import os
import requests
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
question = "mostrar el texto de la siguiente pagina http://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm"

bard = Bard(timeout=30, session=session)  # Set timeout in seconds
result = bard.get_answer(question)['content']
print("Bard replied: ")
print(result)