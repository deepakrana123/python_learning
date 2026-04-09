# def isArmstrong(num):
#     # Write your code here.
#     orginial=num
#     s=len(str(num))
#     sums=0
#     while True:
#         a=num%10
#         sums+=a*a
#         num=num//10
#         if num==0:
#             break
#     return 'Yes' if sums==orginial else 'No'
# print(isArmstrong(13))
def solve(prestart,poststart,preend,preorder,postorder):
    if prestart>preend:
        return None
    
    root=TreeNode(preorder[prestart])
    nextNode=preorder[prestart+1]
    j=poststart
    while postorder[j]!=nextNode:
        j+=1
    num=j-poststart+1
    root.left=solve(prestart+1,poststart,prestart+num,preorder,postorder)
    root.right=solve(prestart+num+1,j+1,preend,preorder,postorder)
    return root
    
def constructFromPrePost(preorder, postorder):
    n=len(preorder)
    return solve(0,0,n-1,preorder,postorder)

        