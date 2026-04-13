from dataclasses import dataclass


@dataclass(frozen=True)
class MarketEvent:
    stock: str
    price: float
    timestamp: float

    def __str__(self):
        return f"{self.stock} (Price:{self.price}) {self.timestamp}"

    def __repr__(self):
        return f"Stock(stock={self.stock}) ,price={self.price} , timestamp={self.timestamp}"


# class Freezeable:
#     def __init__(self):
#         self._frozen = False

#     def freeze(self):
#         self._frozen = True

#     def __setattr__(self, stock, price, timestamp):
#         if hasattr(self, "_frozen") and self._frozen and stock == "_frozen":
#             raise AttributeError(f"Cannot modify {stock}, object is frozen")
#         super().__setattr__(stock, price)

#     def __repr__(self):
#         return f"{self.__class__.__stock__}(frozen={self._frozen})"


# class Market(Freezeable):
#     def __init__(self, stock, price, timestamp):
#         super().__init__()
#         self.stock = stock
#         self.price = price
#         self.timestamp = timestamp

#     def __str__(self):
#         return self.stock
