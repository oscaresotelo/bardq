# import wikipedia
# wikipedia.set_lang("es")
# print(wikipedia.summary("san miguel de Tucumán"))
# print(wikipedia.search("tucuman"))


from duckduckgo_search import DDGS

with DDGS() as ddgs:
    for r in ddgs.text('quien fundo tucuman', region='es-ar', safesearch='Off', timelimit='y'):
        print(r ['content'])
ddgs answers -k holocaust -o json