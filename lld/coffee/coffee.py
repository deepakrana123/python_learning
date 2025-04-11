from enum import Enum


class CoffeType(Enum):
    Espresso = 1
    Cappuccino = 2
    Latte = 3


class Coffee:
    def __init__(self, name, price, recipe):
        self.name = name
        self.price = price
        self.recipe = recipe

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_recipe(self):
        return self.recipe


class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def update_quantity(self, amount):
        self.quantity += amount


class Payment:
    def __init__(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount


class CoffeeMachine:
    _instance = None

    def __init__(self):
        if CoffeeMachine._instance is not None:
            raise Exception("This class is a singleton")
        else:
            CoffeeMachine._instance = self
            self.coffee_menu = []
            self.ingredients = {}
            self._initialize_ingredients()
            self._initialize_coffe_menu()

    @staticmethod
    def get_instance():
        if CoffeeMachine._instance is None:
            CoffeeMachine()
        return CoffeeMachine._instance

    def _initialize_coffee_menu(self):
        esperesso_recipe = {self.ingredients["Coffee"]: 1, self.ingredients["Water"]: 1}
        self.coffee_menu.append(Coffee("Espresso", 2.5, esperesso_recipe))
        cappuccino_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1,
            self.ingredients["Milk"]: 1,
        }
        self.coffee_menu.append(Coffee("Cappuccino", 2.5, cappuccino_recipe))
        latte_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1,
            self.ingredients["Milk"]: 1,
        }
        self.coffee_menu.append(Coffee("Latte", 2.5, latte_recipe))

    def display_menu(self):
        for coffee in self.coffee_menu:
            print(f"{coffee.get_name()}")

    def select_coffe(self, coffe_name):
        for coffee in self.coffee_menu:
            if coffee.get_name().lower() == coffe_name.lower():
                return coffee
        return None

    def dispense_coffee(self, coffee, payment):
        if payment.get_amount() >= coffee.get_price():
            if self.has_enoungh_ingredients(coffee):
                self.update_ingredients(coffee)
                print(f"dispensing {coffee.get_name()}")
                change = payment.get_amount() - coffee.get_price()
                if change > 0:
                    print(f"please collect your chnage")
            else:
                print(f"insufficient ingredients to make")
        else:
            print(f"insufficient payment")

    def _has_enoungh_ingredients(self, coffee):
        for ingredient, required_quantity in coffee.get_recipe().items():
            if ingredient.get_quantity() < required_quantity:
                return False
        return True

    def _update_ingredients(self, coffee):
        for ingredient, required_quantity in coffee.get_recipe().items():
            ingredient.update_quantity(-required_quantity)
            if ingredient.get_quantity() < 3:
                print(f"Low inventory alert: {ingredient.get_name()}")
