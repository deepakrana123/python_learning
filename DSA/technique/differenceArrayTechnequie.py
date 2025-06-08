# difference array technique
#  famous technique use to efficently apply range updates to an array . it helps to do multiple update in constant time
# its an update query  works for apply in range but it works in one go , not in burte force way


arr = [0, 0, 0, 0, 0]
# if queries are in form  [l,r,x] , for mutation do this arr[l]+=x,arr[r+1]-=x :x+1<n, in last take cumulative sum of mutation array


#  segment tree are good when you have to different kind of operations in an array in some range
