# list are ordered , indexed,changeable,and allow duplicate


#  list are created with [ ] symbols

thislist=["1","how","4","why"]
thislist2=list(["1","how","4","why","where"])
thislist2.insert(2,"blackcurrent")
print(len(thislist))
print(thislist[0])
print(thislist[0:2])
print(thislist[0:1:4])
print(type(thislist2))
print(thislist2)

thistuple = ("kiwi", "orange")
thislist2.extend(thistuple)
thislist2.append("have a good day")
thislist2.insert(4,"how can you do this")
print(thislist2,"how")
if "apple" in thislist:
    print("why it is in it")
else:
    print("koun tuuhje you pyar karega")

