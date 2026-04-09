def reverse(nums):
    negative=False
    if(nums<0):
        negative=True
        nums*=-1
    ans=0
    while(nums !=0):
        remainder=nums%10
        ans=ans*10+remainder
        nums=int(nums/10)
    
    if(negative):
        ans*=-1
    
    # print(ans)
    if((ans>(2**31-1)/10) or (ans<(-2**31/10))):
        return 0
    
    return ans

print(reverse(-121234567890706574234250))