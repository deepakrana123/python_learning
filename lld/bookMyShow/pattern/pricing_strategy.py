from datetime import datetime
from datetime import timedelta


class PricingStrategy:
    def calculate_price(self, base_price, show, seat):
        raise NotImplementedError


class DefaultPricing(PricingStrategy):
    def calculate_price(self, base_price, show, seat):
        return base_price


class DynamicPricing(PricingStrategy):
    def calculate_price(self, base_price, show, seat):
        price = base_price
        if show.get_occupancy() > 40:
            price += 40
        if seat.seat_type.name == "VIP":
            price += 20
        return price
