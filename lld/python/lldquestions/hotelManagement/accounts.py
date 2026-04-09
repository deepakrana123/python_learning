from abc import ABC
from .constantEnum import *
from datetime import datetime


class Account:
    def __init__(self, id, password, status=AccountStatus.Active):
        self.__id = id
        self.__password = password
        self.__status = status

    def resetPassword(self, id):
        pass


class Person:
    def __init__(self, name, address, email, phone, account):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__phone = phone
        self.__account = account


class Guest(Person):
    def __init__(self):
        self.__total_rooms_checked_in = 0

    def get_bookings(self):
        None


class Receptionist(Person):
    def search_member(self, name, email, phone):
        None

    def create_booking(self):
        None


class Server(Person):
    def add_room_charge(self, room, room_charge):
        None


class Hotel:
    def __init__(self, name):
        self.name = name
        self.location = []

    def addLocation():
        pass


class HotelLocation:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def getRooms():
        pass


class Search(ABC):
    def search(self, style, start_date, duration):
        None


class Room(Search):
    def __init__(self, roomNumber, style, status, bookingPrice, isSmoking):
        self.roomNumber = roomNumber
        self.style = style
        self.bookingPrice = bookingPrice
        self.status = status
        self.isSmoking = isSmoking
        self.__keys = []
        self.__house_keeping_log = []

    def isRoomAvailable(self, roomNumber):
        return self.status

    def checkIn(self, roomNumber):
        pass

    def checkOut(self):
        pass

    def search(self, style, start_time):
        None


class RoomKey:
    def __init__(self, keyId, barcode, issueAt, active, isMaster):
        self.keyId = keyId
        self.barcode = barcode
        self.active = active
        self.issueAt = issueAt
        self.isMaster = isMaster

    def assignRoom(self):
        pass

    def isActive(self):
        pass


class RoomHouseKeeping:
    def __init__(self, description, duration, house_keeper):
        self.__description = description
        self.__start_datetime = datetime.today()
        self.__duration = duration
        self.__house_keeper = house_keeper

    def add_house_keeping(self, room):
        None


class RoomBooking:
    def __init__(
        self, reservation_number, start_date, duration_in_days, booking_status
    ):
        self.__reservation_number = reservation_number
        self.__start_date = start_date
        self.__duration_in_days = duration_in_days
        self.__status = booking_status
        self.__checkin = None
        self.__checkout = None

        self.__guest_id = 0
        self.__room = None
        self.__invoice = None
        self.__notifications = []

    def fetch_details(self, reservation_number):
        None


class RoomCharge(ABC):
    def __init__(self):
        self.__issue_at = datetime.today()

    def add_invoice_item(self, invoice):
        None


class Amenity(RoomCharge):
    def __init__(self, name, description):
        self.__name = name
        self.__description = description


class RoomService(RoomCharge):
    def __init__(self, is_charge, request_time):
        self.__is_chargeable = is_charge
        self.__request_time = request_time


class KitchenService(RoomCharge):
    def __init__(self, description):
        self.__descripiton = description
