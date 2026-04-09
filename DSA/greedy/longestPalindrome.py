class Solution:
    def longestPalindrome(self, words):
        dictMap = {}
        untouched = False
        result = 0
        
        for word in words:
            if word in dictMap:
                dictMap[word] += 1
            else:
                dictMap[word] = 1
        
        for word in words:
            rev = word[::-1]
            
            if rev != word:
                if dictMap[word] > 0 and dictMap.get(rev, 0) > 0:
                    dictMap[word] -= 1
                    dictMap[rev] -= 1
                    result += 4
            else:
                if dictMap[word] >= 2:
                    dictMap[word] -= 2
                    result += 4
                elif dictMap[word] == 1 and not untouched:
                    dictMap[word] -= 1
                    result += 2
                    untouched = True
        
        return result
