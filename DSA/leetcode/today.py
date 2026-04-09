class ProductOfNumbers:

    def __init__(self):
        self.arr=[]
        self.n=0
        

    def add(self, num: int) -> None:
        if num==0:
            self.arr=[]
            self.n=0
        else:
            if len(self.arr)==0:
                self.arr.append(num)
            else:
                self.arr.append(self.arr[-1]*self.n)
            self.n+=1
        

    def getProduct(self, k: int) -> int:
        if k>self.n:
            return 0
        elif k==self.n:
            return self.arr[self.n-1]
        return self.arr[self.n-1]//self.arr[self.n-k-1]

        
        
def punishmentNumber(n):
    punish=0
    def possible(currInd,currSum,sq,target):
        if currInd==len(sq):
            return currSum==target
        
        if currSum>target:
            return False
        possibleVar=False
        for j in range(currInd,len(sq)):
            subStr = sq[currInd:j+1]  
            val=int(subStr)
            possibleVar=possibleVar or possible(j+1,currSum+val,sq,target)
            if possibleVar:
                return True
        return possibleVar

    for i in range(1,n+1):
        sq=str(i*i)
        if possible(0,0,sq,i):
            punish+=1
    return punish
    
print(punishmentNumber(10))