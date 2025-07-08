from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass


class SimpleCoffe(Coffee):
    def cost(self):
        return 50

    def description(self):
        return "Simple Coffe"


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()


class Milk(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 10

    def description(self):
        return self._coffee.description() + ", Milk"


class Sugar(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 5

    def description(self):
        return self._coffee.description() + ", Sugar"
