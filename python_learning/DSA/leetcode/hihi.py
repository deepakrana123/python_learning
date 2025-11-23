class Solution:
    def decrypt(self, code, k):
        result=[-1]*len(code)
        k=-1*k if k<0 else k
        for i in range(len(code)):
            s=0
            if(k<0):
                for j in range(1,k+1):
                    pointer=(len(code)-k+i+j)%len(code)
                    s+=code[pointer]
            elif k>0:
                for j in range(1,k+1):
                    pointer=(i+j)%len(code)
                    s+=code[pointer]
            else:
                s=0
            result[i]=s
        return result

a=Solution()
print(a.decrypt([5,7,1,4], k = 3))
print(a.decrypt([1,2,3,4], k = 0))
print(a.decrypt([2,4,9,3], k = -2))
        