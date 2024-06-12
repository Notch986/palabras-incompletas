import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;

public class detectorOptimizado {
    private static final double UMBRAL = 0.5;

    public static void main(String[] args) throws IOException {
        String archivoDiccionario = "esp1.txt";
        Set<String> diccionario = cargarDiccionario(archivoDiccionario);

        String[] textos = {
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
        };

        long startTime = System.currentTimeMillis();

        for (String texto : textos) {
            Resultado resultado = contarPalabrasIncorrectas(texto, diccionario, UMBRAL);
            System.out.println("Texto: " + texto);
            System.out.println("Número de palabras incorrectas: " + resultado.numeroIncorrectas);
            System.out.println("Palabras incorrectas: " + resultado.palabrasIncorrectas);
            System.out.println();
        }

        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;
        System.out.printf("Tiempo de ejecución: %.2f segundos\n", elapsedTime / 1000.0);
    }

    // Parte 1: Algoritmo de Levenshtein
    // Esta parte será explicada por la primera persona

    /**
     * Método que calcula la distancia de Levenshtein entre dos cadenas
     * @param s1 Primera cadena
     * @param s2 Segunda cadena
     * @param umbral Umbral para la distancia de Levenshtein
     * @return La distancia de Levenshtein
     */
    private static int distanciaLevenshtein(String s1, String s2, int umbral) {
        int m = s1.length();
        int n = s2.length();
        if (m < n) {
            return distanciaLevenshtein(s2, s1, umbral);
        }

        int[] previousRow = new int[n + 1];
        int[] currentRow = new int[n + 1];

        for (int j = 0; j <= n; j++) {
            previousRow[j] = j;
        }

        for (int i = 1; i <= m; i++) {
            currentRow[0] = i;
            for (int j = 1; j <= n; j++) {
                int insertions = previousRow[j] + 1;
                int deletions = currentRow[j - 1] + 1;
                int substitutions = previousRow[j - 1] + (s1.charAt(i - 1) != s2.charAt(j - 1) ? 1 : 0);
                currentRow[j] = Math.min(insertions, Math.min(deletions, substitutions));
            }
            if (currentRow[minIndex(currentRow)] > umbral) {
                return umbral + 1;
            }
            int[] temp = previousRow;
            previousRow = currentRow;
            currentRow = temp;
        }

        return previousRow[n];
    }

    /**
     * Encuentra el índice del valor mínimo en un array
     * @param array Array de enteros
     * @return Índice del valor mínimo
     */
    private static int minIndex(int[] array) {
        int minIndex = 0;
        for (int i = 1; i < array.length; i++) {
            if (array[i] < array[minIndex]) {
                minIndex = i;
            }
        }
        return minIndex;
    }

    // Parte 2: Verificación de Palabras Incorrectas y Carga del Diccionario
    // Esta parte será explicada por la segunda persona

    /**
     * Método que verifica si una palabra es incorrecta
     * @param palabra La palabra a verificar
     * @param diccionario El conjunto de palabras correctas
     * @param umbral El umbral de distancia de Levenshtein
     * @return Verdadero si la palabra es incorrecta, falso si es correcta
     */
    private static boolean esPalabraIncorrecta(String palabra, Set<String> diccionario, double umbral) {
        if (diccionario.contains(palabra)) {
            return false;
        }
        int palabraLen = palabra.length();
        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        List<Future<Boolean>> resultados = new ArrayList<>();

        for (String palabraCorrecta : diccionario) {
            resultados.add(executor.submit(() -> {
                if (Math.abs(palabraCorrecta.length() - palabraLen) > umbral * palabraLen) {
                    return true;
                }
                return distanciaLevenshtein(palabra, palabraCorrecta, (int) (umbral * palabraLen)) > umbral * palabraLen;
            }));
        }

        executor.shutdown();
        try {
            for (Future<Boolean> resultado : resultados) {
                if (!resultado.get()) {
                    return true;
                }
            }
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }

        return false;
    }

    /**
     * Carga el diccionario desde un archivo
     * @param archivo Ruta del archivo
     * @return Un conjunto de palabras del diccionario
     * @throws IOException Si ocurre un error al leer el archivo
     */
    private static Set<String> cargarDiccionario(String archivo) throws IOException {
        return new HashSet<>(Files.readAllLines(Paths.get(archivo)));
    }

    /**
     * Limpia el texto eliminando caracteres no alfanuméricos y convirtiéndolo a minúsculas
     * @param texto Texto a limpiar
     * @return Texto limpio
     */
    private static String limpiarTexto(String texto) {
        return texto.toLowerCase().replaceAll("[^\\w\\s]", "");
    }

    // Parte 3: Función Principal (main) que Cuenta las Palabras Incorrectas y Mide el Tiempo de Ejecución
    // Esta parte será explicada por la tercera persona

    /**
     * Cuenta las palabras incorrectas en un texto
     * @param texto El texto a analizar
     * @param diccionario El conjunto de palabras correctas
     * @param umbral Umbral para la distancia de Levenshtein
     * @return Un objeto Resultado con el número de palabras incorrectas y la lista de palabras incorrectas
     */
    private static Resultado contarPalabrasIncorrectas(String texto, Set<String> diccionario, double umbral) {
        String textoLimpio = limpiarTexto(texto);
        String[] palabras = textoLimpio.split("\\s+");
        int palabrasIncorrectas = 0;
        List<String> detallesIncorrectos = new ArrayList<>();

        for (String palabra : palabras) {
            if (esPalabraIncorrecta(palabra, diccionario, umbral)) {
                palabrasIncorrectas++;
                detallesIncorrectos.add(palabra);
            }
        }

        return new Resultado(palabrasIncorrectas, detallesIncorrectos);
    }

    /**
     * Clase para almacenar el resultado del análisis de palabras incorrectas
     */
    private static class Resultado {
        int numeroIncorrectas;
        List<String> palabrasIncorrectas;

        Resultado(int numeroIncorrectas, List<String> palabrasIncorrectas) {
            this.numeroIncorrectas = numeroIncorrectas;
            this.palabrasIncorrectas = palabrasIncorrectas;
        }
    }
}
