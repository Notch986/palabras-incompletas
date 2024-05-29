import nltk
nltk.download('cess_esp')

from nltk.corpus import cess_esp
import re

# Cargar las palabras del corpus
words = cess_esp.words()

# Definir una función para eliminar caracteres especiales
def remove_special_characters(word):
    return re.sub(r'[^a-zA-Z]', '', word)

# Filtrar las palabras y eliminar caracteres especiales
filtered_words = [remove_special_characters(word) for word in words if remove_special_characters(word)]

# Guardar las palabras filtradas en un archivo de texto
with open('palabras_esp.txt', 'w', encoding='utf-8') as f:
    for word in filtered_words:
        f.write(word + '\n')

