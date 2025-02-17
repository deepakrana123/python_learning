import copy

# class Prototype:
#     def clone(self):
#         return copy.deepcopy(self)

# class Car(Prototype):
#     def __init__(self,model,color):
#         self.model=model
#         self.color=color
#     def display(self):
#         """Displays car details."""
#         print(f"Car Model: {self.model}, Color: {self.color}")


# if __name__ == "__main__":
#     original_car = Car("Tesla Model S", "Red")
#     cloned_car = original_car.clone()
#     cloned_car.color = "Blue"
#     original_car.display()
#     cloned_car.display()

# class Prototype:
#     def clone(self):
#         return copy.deepcopy(self)
# class Student(Prototype):
#     def __init__(self,name,age,grades):
#         self.name=name
#         self.age=age
#         self.grades=grades
#     def display(self):
#         """Displays car details."""
#         print(f"Student name: {self.name}, age: {self.age},grades:{self.grades}")
# if __name__ == "__main__":
#     original_car = Student("Devendra", "23","A")
#     cloned_car = original_car.clone()
#     cloned_car.age = "29"
#     original_car.display()
#     cloned_car.display()

class PrototypeS:
    def clone(self):
        return copy.deepcopy(self)
    def shallow(self):
        return copy.copy(self)

class S(PrototypeS):
    def __init__(self,name,age,grades):
        self.name=name
        self.age=age
        self.grades=grades
    def display(self):
        """Displays car details."""
        print(f"Student name: {self.name}, age: {self.age},grades:{self.grades}")
if __name__ == "__main__":
    original_car = S("Devendra",{"Maths":'A',"Sceience":'B'}, "23")
    cloned_car = original_car.clone()
    cloned_car.age['Maths'] = "D"
    shallow_car=original_car.shallow()
    shallow_car.age['Maths']='F'
    shallow_car.display()
    original_car.display()
    cloned_car.display()


class User:
    def __init__(self,name):
        self.name=name
    def getName(self):
        return self.name

class Regisitery_clone:
    
