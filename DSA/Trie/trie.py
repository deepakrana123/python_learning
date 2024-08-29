class TrieNode:
    def __init__(self):
        self.is_end_of_word=False
        self.children={}
class Trie:

    def __init__(self):
        self.root=TrieNode()
    def insert(self, word: str) -> None:
        crawl=self.root
        for char in word:
            if char not in crawl.children:
                crawl.children[char]=TrieNode()
            crawl=crawl.children[char]
        crawl.is_end_of_word = True
        

    def search(self, word: str) -> bool:
        crwal = self.root
        for char in word:
            if char not in crwal.children:
                return False
            crwal = crwal.children[char]
        return crwal.is_end_of_word
        

    def startsWith(self, prefix: str) -> bool:
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True
    def delete(self, word):
        def _delete(current_node, word, depth):
                if depth == len(word):
                    # Word found, set the end of word to False
                    if not current_node.is_end_of_word:
                        return False  # Word not found
                    current_node.is_end_of_word = False
                    # If the current node has no other children, delete it
                    return len(current_node.children) == 0

                char = word[depth]
                if char not in current_node.children:
                    return False  # Word not found

                can_delete_child = _delete(current_node.children[char], word, depth + 1)

                if can_delete_child:
                    # Remove the child node
                    del current_node.children[char]
                    # Return True if the current node can also be deleted
                    return len(current_node.children) == 0 and not current_node.is_end_of_word

                return False
        _delete(self.root, word, 0)


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)