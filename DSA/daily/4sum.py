class Solution:
    def areSentencesSimilar(self, sentence1: str, sentence2: str) -> bool:
        s1 = sentence1.split(' ')
        s2 = sentence2.split(' ')
        if len(s1) < len(s2):
            s1, s2 = s2, s1
        start1, start2 = 0, 0
        end1, end2 = len(s1) - 1, len(s2) - 1
        while start2 <= end2 and s1[start1] == s2[start2]:
            start1 += 1
            start2 += 1
        while start2 <= end2 and s1[end1] == s2[end2]:
            end1 -= 1
            end2 -= 1
        return  start2 > end2
            

a=Solution()
print(a.areSentencesSimilar( "of", "A lot of words"))
        
        