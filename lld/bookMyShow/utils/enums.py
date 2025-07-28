from enum import Enum


class SeatType(Enum):
    VIP, SUBVIP, NORMAL = 1, 2, 3


class Status(Enum):
    AVAIABLE, RESERVED, BOOKED, HOLD = 1, 2, 3, 4
