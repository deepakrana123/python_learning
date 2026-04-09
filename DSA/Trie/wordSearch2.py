class TrieNode:
    def __init__(self):
        self.is_end_of_word = False
        self.children = {}
        self.words = ""


class Solution:
    def __init__(self):
        self.result = []
        self.m = 0
        self.n = 0
        self.root = TrieNode()

    def insertInTrie(self, word):
        pCrwal = self.root
        for char in word:
            if char not in pCrwal.children:
                pCrwal.children[char] = TrieNode()
            pCrwal = pCrwal.children[char]
        pCrwal.is_end_of_word = True
        pCrwal.words = word

    def findWord(self, board, index, jndex, root):
        if index < 0 or index >= self.m or jndex < 0 or jndex >= self.n:
            return
        if board[index][jndex] == '$' or board[index][jndex] not in root.children:
            return
        root = root.children[board[index][jndex]]
        if root.is_end_of_word == True:
            self.result.append(root.words)
            root.is_end_of_word = False
        temp = board[index][jndex]
        board[index][jndex] = '$'
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for dir in dirs:
            x, y = dir
            new_x = index+x
            new_y = jndex+y
            self.findWord(board, new_x, new_y, root)
        board[index][jndex] = temp

    def findWords(self, board, words):
        self.m = len(board)
        self.n = len(board[0])
        for word in words:
            self.insertInTrie(word)
        for i in range(self.m):
            for j in range(self.n):
                ch = board[i][j]
                if ch in self.root.children:
                    self.findWord(board, i, j, self.root)
        return self.result



