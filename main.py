import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return "invalid"
            node = node.children[char]
        if node.is_end_of_word:
            return "complete"
        else:
            return "incomplete"

def load_spanish_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [word.strip().lower() for word in file]

def analyze_text(text, trie):
    words = text.split()
    incomplete_count = 0
    incomplete_words = []
    for word in words:
        result = trie.search(word.lower())
        if result == "incomplete":
            incomplete_count += 1
            incomplete_words.append(word)
    return incomplete_count, incomplete_words

# Ejemplo de uso
# Cargar las palabras en español desde un archivo
spanish_words = load_spanish_words('esp1.txt')

# Medir el tiempo de carga del Trie
start_time = time.time()
trie = Trie()
for word in spanish_words:
    trie.insert(word)
end_time = time.time()
print(f"Tiempo de carga del Trie: {end_time - start_time} segundos")


# Analizar un texto
text = "el trbajo esta inompleto poque fe rpido"
incomplete_count, incomplete_words = analyze_text(text, trie)

print(f"El texto tiene {incomplete_count} palabras incompletas: {', '.join(incomplete_words)}")
