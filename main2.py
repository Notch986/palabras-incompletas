import nltk
nltk.download('punkt')

from spellchecker import SpellChecker

def analizar_texto(input_text):
    # Configuramos el corrector ortográfico en español
    spell = SpellChecker(language='es')
    
    # Tokenizamos el texto en palabras
    palabras = nltk.word_tokenize(input_text)
    
    # Encontramos las palabras que están mal escritas
    palabras_incorrectas = spell.unknown(palabras)
    
    # Contamos las palabras incorrectas
    num_incorrectas = len(palabras_incorrectas)
    
    # Corregimos el texto
    texto_corregido = ' '.join([spell.correction(palabra) if palabra in palabras_incorrectas else palabra for palabra in palabras])
    
    return num_incorrectas, texto_corregido

# Texto de entrada
input_text = "El trbajo eta inompleto poqe fue apido"

# Análisis del texto
num_incorrectas, texto_corregido = analizar_texto(input_text)
print(f"{num_incorrectas} palabras incompletas; el texto sería: {texto_corregido}")
