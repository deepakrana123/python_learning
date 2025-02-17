class Car:
    def __init__(self) -> None:
        self.model=None
        self.color=None
        self.engine=None
    def __str__(self):
        return f"carModel:{self.model}, engine:{self.engine},color:{self.color}"
    
# abstract build interface
# used for code consistency only , if i have a specific cla
class CarBuilder:
    def set_model(self):
        pass
    def set_color(self):
        pass
    def set_engine(self):
        pass
    def get_car(self):
        pass


class SportsCarBuilder(CarBuilder):
    def __init__(self):
        self.car=Car()
    def set_model(self,model):
        self.car.model=model
        return self
    def set_color(self,color):
        self.car.color=color
        return self
    def set_engine(self,engine):
        self.car.engine=engine
        return self
    def get_car(self):
        return self.car
    
class CarDirector:
    def __init__(self, builder):
        self.builder = builder

    def build_car(self, model, color, engine):
        return self.builder.set_model(model).set_color(color).set_engine(engine).get_car()
builder = SportsCarBuilder()
director = CarDirector(builder)
car = director.build_car("Ferrari", "Red", "V8")
print(car)



# class Computer:
#     def __init__(self):
#         self.CPU = None
#         self.RAM = None
#         self.GPU = None
#         self.stroage = None
#     def __str__(self):
#         return f"ComputerCPU:{self.CPU}, GPU:{self.GPU},RAM:{self.RAM},Stroage:{self.stroage}"
    
# # abstract build interface
# # used for code consistency only , if i have a specific cla
# class ComputerBuilder:
#     def set_CPU(self):
#         pass
#     def set_RAM(self):
#         pass
#     def set_GPU(self):
#         pass
#     def set_stroage(self):
#         pass
#     def get_computer(self):
#         pass

# class GamingPCBuilder(ComputerBuilder):
#     def __init__(self):
#         self.computer = Computer()
#     def set_CPU(self,CPU):
#         self.computer.CPU = CPU
#         return self
#     def set_RAM(self,RAM):
#         self.computer.RAM = RAM
#         return self
#     def set_GPU(self,GPU):
#         self.computer.GPU = GPU
#         return self
#     def set_stroage(self,stroage):
#         self.computer.stroage = stroage
#         return self
#     def get_computer(self):
#         return self.computer
    
# class ComputerDirector:
#     def __init__(self, builder):
#         self.builder = builder
#     def build_car(self, model, color, engine,stroage):
#         return self.builder.set_CPU(model).set_RAM(color).set_GPU(engine).set_stroage(stroage).get_car()
# builder = GamingPCBuilder()
# director = ComputerDirector(builder)
# car = director.build_car("12", "Redv4", "V81","256")
# print(car)



# class Meals:
#     def __init__(self):
#         self.Meal = None
#         self.Side = None
#         self.Drink = None
#     def __str__(self):
#         return f"Meal:{self.Meal}, Side:{self.Side},Drink:{self.Drink}"

# class MealsAbstract:
#     def add_meals(self,meal):
#         return self
#     def add_side_food(self,food):
#         return self
#     def add_drinks(self,drink):
#         return self

# class FastFoodMeals(MealsAbstract):
#     def __init__(self):
#         self.meal=Meals()
#     def add_meals(self,Meal):
#         self.meal.Meal=Meal
#         return self
#     def add_side_food(self,Side):
#         self.meal.Side=Side
#         return self
#     def add_drinks(self,drinks):
#         self.meal.Drink=drinks
#         return self
#     def get_meals(self):
#         return self.meal

# class HealthFoodMeals(MealsAbstract):
#     def __init__(self):
#         self.meal=Meals()
#     def add_meals(self,Meal):
#         self.meal.Meal=Meal
#         return self
#     def add_side_food(self,Side):
#         self.meal.Side=Side
#         return self
#     def add_drinks(self,drinks):
#         self.meal.Drink=drinks
#         return self
#     def get_meals(self):
#         return self.meal
# class MealsDirector:
#     def __init__(self, builder):
#         self.builder = builder
#     def build_meal(self, meal, sideFood, drinks):
#         return self.builder.add_meals(meal).add_side_food(sideFood).add_drinks(drinks).get_meals()

    
# fastFoodBuilder = FastFoodMeals()
# healthBuilder=HealthFoodMeals()
# director = MealsDirector(fastFoodBuilder)
# director1 = MealsDirector(healthBuilder)
# meal = director.build_meal("Burger","French Fries",'Cocola')
# print(meal)
    




