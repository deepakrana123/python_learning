class Solution:
    def convertDateToBinary(self,date):
        s=date.split('-')
        a=""
        for i in range(len(s)):
            if s[i][0]=='0':
                a+=bin(int(s[i][1:]))[2:]+'-'
            else:
                a+=bin(int(s[i]))[2:]+'-'
        return a[0:len(a)-1].lstrip('0')
a=Solution()
print(a.convertDateToBinary("2080-02-29"))
    
        
        

            
            
        
        
        
            
        
        