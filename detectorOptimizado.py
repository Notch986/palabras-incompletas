import re
import nltk
import time
from concurrent.futures import ThreadPoolExecutor
from nltk.corpus import cess_esp
import os

if not os.path.join(nltk.data.path[0], 'cess_esp'):
    nltk.download('cess_esp')

def distancia_levenshtein(s1, s2, umbral):
    m, n = len(s1), len(s2)
    if m < n:
        return distancia_levenshtein(s2, s1, umbral)

    previous_row = range(n + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        if min(current_row) > umbral:
            return umbral + 1  # Si la mínima distancia supera el umbral, no es necesario continuar
        previous_row = current_row

    return previous_row[-1]

def es_palabra_incorrecta(palabra, diccionario, umbral=0.5):
    if palabra in diccionario:
        return False
    palabra_len = len(palabra)
    with ThreadPoolExecutor() as executor:
        resultados = list(executor.map(lambda palabra_correcta: abs(len(palabra_correcta) - palabra_len) > umbral or
                                                          distancia_levenshtein(palabra, palabra_correcta, umbral) > umbral, diccionario))
    return all(resultados)

def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def contar_palabras_incorrectas(texto, diccionario, umbral=0):
    texto_limpio = limpiar_texto(texto)
    palabras = texto_limpio.split()
    palabras_incorrectas = 0
    detalles_incorrectos = []

    for palabra in palabras:
        if es_palabra_incorrecta(palabra, diccionario, umbral):
            palabras_incorrectas += 1
            detalles_incorrectos.append(palabra)

    return palabras_incorrectas, detalles_incorrectos

def cargar_diccionario(archivo):
    with open(archivo, 'r', encoding='utf-8') as file:
        diccionario = set(file.read().splitlines())  # Usar set para búsquedas rápidas
    return diccionario

def cargar_diccionario_nltk():
    palabras = cess_esp.words()
    diccionario = set(palabras)
    return diccionario

# Cargar diccionario desde nltk
#diccionario = cargar_diccionario_nltk()

# Medir el tiempo de ejecución
start_time = time.time()

archivo_diccionario = 'esp3.txt'

textos = [
    "El trbajo eta inompleto poqe fue apido",
    "La combnicación de cocolates y flores fué ideal",
    "Me gustaría comprar un perro de raca pequeña",
    "Estoy deseando probar esa nuva marca de helado",
    "No entendí el acertijo, era demaciado complicado",
    "Mi hermano compitió en una competición de artes marciales",
    "El café estava delicioso, no me gusto el pastel",
    "El estudiante tenía que entregar un travajo muy extenso",
    "Fuimos al cine pero la película estubo aburrida",
    "Esa novela tiene una trama apasionante, la recomiendo",
]

for texto in textos:
    palabras_incorrectas, detalles_incorrectos = contar_palabras_incorrectas(texto, cargar_diccionario_nltk())
    print(f"Texto: {texto}")
    print(f"Número de palabras incorrectas: {palabras_incorrectas}")
    print(f"Palabras incorrectas: {detalles_incorrectos}")
    print()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")
