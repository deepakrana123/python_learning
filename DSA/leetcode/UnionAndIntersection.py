def intersection():
    ar1=[3,4,6,7,10, 12, 5]
    ar2=[7,11,15, 18]
    ar3=[]
    for i in range(0,len(ar1)):
        for j in range(0,len(ar2)):
            if(ar1[i]==ar2[j]):
                if(ar1[i]  not in ar3):
                 ar3.append(ar1[i])
    return ar3

print(intersection())


def binary_search(arr,size,element):
   start=0
   end=size
   while(end>=start):
      mid=int(start+(end-start)/2)
      if(arr[mid]==element):
         return True
      elif(arr[mid]>element):
         end=mid-1
      else:
         start=mid+1

   return False

def intersections(arr1,arr2):
   arr2.sort()
   arr3=[]
   for i in range(0,len(arr1)-1):
      if(binary_search(arr2,len(arr2)-1,arr1[i])):
         arr3.append(arr1[i])
         return arr3

print(intersections([0,9,2,4],[2,3,5,1]))


def twopointersapproach(arr1,arr2):
   arr1.sort()
   arr2.sort()
   arr3=[]
   i,j=0,0
   while(i<len(arr1) and j<len(arr2)):
      if(arr1[i]==arr2[j] and arr1[i] not in arr3):
         arr3.append(arr1[i])
         print(arr3)
         i+=1
         j+=1
      elif(arr1[i]>arr2[j]):
         j+=1
      else:
         i+=1
         return arr3
   
print(twopointersapproach([0,9,2,4],[2,3,5,1]))