import re
from collections import defaultdict, Counter

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

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def suggestions_from_node(self, node, prefix):
        suggestions = []
        self._dfs(node, prefix, suggestions)
        return suggestions

    def _dfs(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append(prefix)
        for char, next_node in node.children.items():
            self._dfs(next_node, prefix + char, suggestions)

def load_words_from_file(file_path):
    trie = Trie()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            trie.insert(word)
    return trie

def load_bigrams(file_path):
    bigrams = defaultdict(Counter)
    with open(file_path, 'r', encoding='utf-8') as file:
        previous_word = None
        for line in file:
            for word in re.findall(r'\b\w+\b', line.lower()):
                if previous_word:
                    bigrams[previous_word][word] += 1
                previous_word = word
    return bigrams

def complete_word(trie, incomplete_word, context_word, bigrams):
    node = trie.search(incomplete_word)
    if not node:
        return incomplete_word
    suggestions = trie.suggestions_from_node(node, incomplete_word)
    if not suggestions:
        return incomplete_word
    if context_word and context_word in bigrams:
        ranked_suggestions = sorted(suggestions, key=lambda w: bigrams[context_word][w], reverse=True)
        return ranked_suggestions[0]
    return suggestions[0]

def complete_sentence(trie, bigrams, sentence):
    words = sentence.split()
    completed_words = []
    previous_word = None
    for word in words:
        completed_word = complete_word(trie, word, previous_word, bigrams)
        completed_words.append(completed_word)
        previous_word = completed_word.lower()
    return ' '.join(completed_words)

# Cargar las palabras del archivo y construir el trie y los bigramas
file_path = 'palabras_esp.txt'  # Asegúrate de tener este archivo con palabras en español
trie = load_words_from_file(file_path)
bigrams = load_bigrams(file_path)

# Ejemplo de uso
# sentence = "Quero progr una compu con inteli artif"
sentence = "El trbajo esta inompleto poqye fue apido"
completed_sentence = complete_sentence(trie, bigrams, sentence)
print(completed_sentence)

