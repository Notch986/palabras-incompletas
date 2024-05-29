import nltk
from nltk.corpus import words
from collections import defaultdict

# Descargar el corpus de palabras (en caso de que exista un corpus específico de español)
nltk.download('words')

# Supongamos que tenemos un archivo con palabras en español llamado "spanish_words.txt"
# Aquí cargamos las palabras desde un archivo de texto para la demostración
def load_spanish_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)

# Cargamos las palabras en español desde el archivo
spanish_words = load_spanish_words('esp2.txt')

# Construimos un diccionario de prefijos válidos
prefixes = defaultdict(set)
for word in spanish_words:
    for i in range(1, len(word) + 1):
        prefixes[word[:i]].add(word)

def analyze_text(text, words_set, prefixes_dict):
    words = text.split()
    incomplete_count = 0
    incomplete_words = []
    for word in words:
        word_lower = word.lower()
        if word_lower in words_set:
            continue  # Palabra completa
        elif word_lower in prefixes_dict:
            incomplete_count += 1
            incomplete_words.append(word)
        else:
            continue  # Palabra inválida
    return incomplete_count, incomplete_words

# Ejemplo de uso
text = "prro incmpleto gato ca perro per"
incomplete_count, incomplete_words = analyze_text(text, spanish_words, prefixes)

print(f"El texto tiene {incomplete_count} palabras incompletas: {', '.join(incomplete_words)}")
