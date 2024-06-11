import numpy as np
import re

def distancia_levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = np.zeros((m+1, n+1), dtype=int)
    
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
        
    for i in range(1, m+1):
        for j in range(1, n+1):
            costo = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j] + 1,    # Eliminación
                           dp[i][j-1] + 1,    # Inserción
                           dp[i-1][j-1] + costo)  # Sustitución
    
    return dp[m][n]

def es_palabra_incorrecta(palabra, diccionario, umbral=0):
    return all(distancia_levenshtein(palabra, palabra_correcta) > umbral for palabra_correcta in diccionario)

def limpiar_texto(texto):
    texto = texto.lower()  # Convertir a minúsculas
    texto = re.sub(r'[^\w\s]', '', texto)  # Eliminar puntuación
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
        diccionario = file.read().splitlines()
    return diccionario

# Cargar diccionario desde el archivo de texto
archivo_diccionario = 'esp1.txt'
diccionario = cargar_diccionario(archivo_diccionario)

# Texto a analizar
texto = "El trbajo eta inompleto poqe fue apido"

# Contar palabras incorrectas con umbral 0 para mayor exactitud
umbral = 0
palabras_incorrectas, detalles_incorrectos = contar_palabras_incorrectas(texto, diccionario, umbral)
print(f"Número de palabras incorrectas: {palabras_incorrectas}")
print(f"Palabras incorrectas: {detalles_incorrectos}")
