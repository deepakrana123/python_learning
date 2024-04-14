from collections import deque 
def timeRequiredToBuy(tickets, k):
    count=0
    for i in range(len(tickets)):
        if i<=k and tickets[i]<=tickets[k]:
            count+=min(tickets[i],tickets[k]) 
        elif i<=k and tickets[i]>tickets[k]:
            count+=min(tickets[i],tickets[k]) 
    return count      
            
def deckRevealedIncreasing(deck):
    deck.sort()
    a=[0]*len(deck)
    # j=0
    # i=0
    # skip=False
    # while(i<len(deck)):
    #     if a[j]==0:
    #         if skip==False:
    #             a[j]=deck[i]
    #             i+=1
    #         skip=not skip
    #     j=(j+1)%len(deck)
    # return a
    queue=deque([])
    for i in range(len(deck)):
        queue.append(i)
    for i in range(len(deck)):
        d=queue.popleft()
        a[d]=deck[i]
        if(queue):
            e=queue.popleft()
            queue.append(e)
            
    return a
def removeKdigits(num, k):
    a=[]
    for i in range(len(num)):
        if len(a) > 0  and a[len(a)-1] > num[i] and k > 0:
            print(num[i],"a")
            a.pop()
            k=k-1
        elif a or num[i]!=0:
            a.append(num[i])
    print(a,k)
    while k>0 and a:
        a.pop()
        k-=1
    if len(a)==0:
        return 0
    return "".join(a)
                
print(removeKdigits("1432219",3))
    
    
    
            
            
            
        
        
        
    
print(deckRevealedIncreasing([17,13,11,2,3,5,7]
))