def shuffleNegativeAndPostive(arr):
    a=set(arr)
    b=arr.sort()
    return (a,b)

print(shuffleNegativeAndPostive([2,3,-1,9,-10,-13,21]))


def twopointer(arr):
    start,end=0,len(arr)-1
    while(start<end):
      if(arr[start]<0 and arr[end]):
         start+=1
      elif(arr[start]<0 and arr[end]>0):
         arr[start],arr[end]=arr[end],arr[start]
         start+=1
         end-=1
      elif(arr[start]>0 and arr[end]>0):
         end-=1
      else:
         start+=1
         end-=1

    print(arr)
print(twopointer([2,3,-1,9,-10,-13,21]))