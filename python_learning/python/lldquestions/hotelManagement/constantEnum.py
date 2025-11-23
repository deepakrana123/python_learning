from enum import Enum


class RoomStyle(Enum):
    Standard, Deluxe, FamilySuite, BussinessSuite = 1, 2, 3, 4


class PaymentStatus(Enum):
    (
        Unpaid,
        Pending,
        Completed,
        Failed,
        Declined,
        Cancelled,
        Abdandoned,
        Selling,
        Settled,
        Refunded,
    ) = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


class RoomStatus(Enum):
    Available, Reserved, Occupied, NotAvaliable, BeingServiced, Other = 1, 2, 3, 4, 5, 6


class BookingStatus(Enum):
    Requested, Pending, Confirmed, CheckedIn, CheckedOut, Canceled, Abandoned = (
        1,
        2,
        3,
        4,
        5,
        6,
        7,
    )


class AccountStatus(Enum):
    Active, Cancelled, Closed, Backlisted = 1, 2, 3, 4


class AccountType(Enum):
    Member, Guest, Manager, Recpionist = 1, 2, 3, 4


class Address:
    def __init__(self, streetAddress, zipcode, state, city, country):
        self.streetAddress = streetAddress
        self.zipcode = zipcode
        self.state = state
        self.city = city
        self.country = country
