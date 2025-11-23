class TrieNode:
    def __init__(self):
        self.is_end_of_word = False
        self.children = {}

        


class Solution:
    def __init__(self):
            self.root = TrieNode()
    def addWord(self, word: str) -> None:
        crawl = self.root
        for char in word:
            if char not in crawl.children:
                crawl.children[char] = TrieNode()
            crawl = crawl.children[char]
        crawl.is_end_of_word = True
    def search(self,s,start,memo):
        if start in memo:
            return memo[start]
        crawl=self.root
        for i in range(start,len(s)):
            if s[i] not in crawl.children:
                memo[start]=False
                return False
            crawl = crawl.children[s[i]]
            if crawl.is_end_of_word:
                if start==len(s)-1 or self.search(s,i+1,memo):
                    memo[start]=True
                    return True
        memo[start]=False
        return False
    def wordBreak(self, s: str, wordDict):
        for word in wordDict:
            self.addWord(word)
        memo={}
        return self.search(s,0,memo)
a=Solution()
print(a.wordBreak("leetcode", wordDict = ["leet","code"]))
        
# class MagicDictionary:
#     def __init__(self):
#         self.root = TrieNode()
#     def addWord(self, word: str) -> None:
#         crawl = self.root
#         for char in word:
#             if char not in crawl.children:
#                 crawl.children[char] = TrieNode()
#             crawl = crawl.children[char]
#         crawl.is_end_of_word = True

#     def buildDict(self, dictionary) -> None:
#         for word in dictionary:
#             self.addWord(word)
#     def search_utils(self,node,searchWord,index,misMatch):
#         if len(searchWord)==index:
#             if misMatch==1 and node.is_end_of_word:
#                 return True
#             return False
#         currChar=searchWord[index]
#         for char, child_node in node.children.items():
#             if currChar==char:
#                 self.search_utils(node.children[currChar],index+1,misMatch)
#             else:
#                 if misMatch==0:
#                     self.search_utils(node.children[currChar],index+1,misMatch+1)
                    
#     def search(self, searchWord: str) -> bool:
#         return self.search_utils(self.root, searchWord,0,0)

        
        
        