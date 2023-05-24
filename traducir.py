from translate import Translator

def translate_to_english(text):
    translator = Translator(to_lang="en", from_lang="es")
    translation = translator.translate(text)
    return translation

texto = "cuando nacio Belgrano"
print(translate_to_english(texto))