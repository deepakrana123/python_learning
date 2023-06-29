# A tuple is a collection which is ordered and unchangeable and allow duplicate values.
# tuple are indexed they are allowed to have duplicate values

thistuple=tuple(("apple", "banana", "cherry","apples", "bananas", "cherrys","applee", "bananae", "cherrye",))
print(thistuple)

thistuple1=("apple", "banana", "cherry")
print(thistuple1)


# you can change the tuple or remove or add the values in the tuple by changeing it to the list first
# unpacking with tuple

(a,b,*c)=thistuple
(aa,*bb,cc)=thistuple1
# print(aa)
# print(bb)
# print(cc)
# print(a)
# print(b)
# print(c)

for i in range(len(thistuple)):
    print(i,thistuple[i])

thistuple2=thistuple+thistuple1
print(thistuple2)