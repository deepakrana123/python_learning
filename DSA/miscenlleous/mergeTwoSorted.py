def mergeTwoSorted(arr1,arr2):
    for i in range(0,len(arr2)):
        arr1.append(arr2[i])

    return arr1

print(mergeTwoSorted([1,2,3,4,5],[6,7,8,9,10]))

# time complexity o(n)

def mergeTwoSortedOne(arr1,arr2):
     left=len(arr1)
     right=len(arr2)
     if(left<right):
         arr2.append()


print(mergeTwoSortedOne([1,2,3,4,5],[6,7,8,9,10]))


