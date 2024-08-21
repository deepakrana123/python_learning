def minWindow( s, t):
    map={}
    for value in t:
        # if value in map:
        #     map[value]=map[value]+1
        # else:
        #     map[value]=1
        map[value]=map.get(value,0)
    start=0
    end=0
    minStart=0
    minLength=float("inf")
    counter=len(map)
    while end<=len(s):
        val=s[end]
        if map[val]>0:
            counter-=1
        map[val]-=1
        end+=1
        
        while counter==0:
            if end-start<minLength:
                minLength=end-start
                minStart=start
            c2=s[start]
            map[c2]+=1
            if map.get(c2)>0:
                counter+=1
            start+=1
    return "" if minLength==float("inf") else s[minStart,minStart+minLength] 
            
                
                
        

print(minWindow("","ABC"))