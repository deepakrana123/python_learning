# a method to print or add the all element of an array with some condition on it

# it oofer shorter syntax when you wants to create new list form the existing one


fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist=[]
for x in fruits:
    if "a" in x:
        newlist.append(x)
print(newlist)

# in one line

newlist2=[x for x in fruits if "a" in x]
print(newlist2)

# syntax for list comperhension is
# newlist = [expression(outcome) for item in iterable if condition == True]

newlist3=[item for item in fruits if "b" in item ]
print(newlist3)

newlist4=[x for x in fruits]
print(newlist4)

newlist5=["hello" for x in fruits]
print(newlist5)

# copy or creating a new list with the help of the older list you can create a new list , without making the refernce of the older list





