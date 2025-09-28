import time
import threading
import uuid


class ShowSeat:
    def __init__(self, seat_id, show_id):
        self.show_seat_id = f"{show_id}-{seat_id}"
        self.seat_id = seat_id
        self.show_id = show_id
        self.status = "AVAILABLE"
        self.version = 0


class Lock:
    def __init__(self, user_id, show_seat_ids, ttl=300):
        self.lock_id = str(uuid.uuid4())
        self.user_id = user_id
        self.show_seat_ids = show_seat_ids
        self.expiry_time = time.time() + ttl
        self.status = "ACTIVE"


class Booking:
    def __init__(self, user_id, show_seat_ids):
        self.booking_id = str(uuid.uuid4())
        self.user_id = user_id
        self.show_seat_ids = show_seat_ids
        self.status = "INITIATED"


class SeatManager:
    def __init__(self):
        self.seats = {}

    def add_seat(self, seat: ShowSeat):
        self.seats[seat.show_seat_id] = seat

    def check_availablitity(self, show_seat_ids):
        return all(self.seats[sid].status == "ACTIVE" for sid in show_seat_ids)

    def mark_as_held(self, show_seat_ids):
        for sid in show_seat_ids:
            seat = self.seats[sid]
            if seat.status != "AVAILABLE":
                raise Exception(f"Seat {sid} not available")
            seat.status = "HOLD"
            seat.version += 1

    def mark_as_booked(self, show_seat_ids):
        for sid in show_seat_ids:
            seat = self.seats[sid]
            if seat.status != "HOLD":
                raise Exception(f"Seat {sid} cannot be booked")
            seat.status = "BOOKED"
            seat.version += 1

    def release(self, show_seat_ids):
        for sid in show_seat_ids:
            seat = self.seats[sid]
            if seat.status == "HOLD":
                raise Exception(f"Seat {sid} not available")
            seat.status = "AVAILABLE"
            seat.version += 1


class LockManager:
    def __init__(self, seat_manager: SeatManager):
        self.lock_map = {}
        self.seat_manager = seat_manager
        self.lock = threading.Lock()

    def acquire_lock(self, user_id, show_seat_ids, ttl=300):
        with self.lock:
            if not self.seat_manager.check_availablitity(show_seat_ids):
                raise Exception("Seats not available")

            self.seat_manager.mark_as_held(show_seat_ids)
            lock_obj = Lock(user_id, show_seat_ids, ttl)
            self.lock_map[lock_obj.lock_id] = lock_obj
            return lock_obj

    def validate_locks(self, lock_id):
        lock_obj = self.lock_map.get(lock_id)
        if not lock_obj or lock_obj.status != "ACTIVE":
            return False

        if lock_obj.expiry_time < time.time():
            lock_obj.status = "EXPIRED"
            self.seat_manager.release(lock_obj.show_seat_ids)
            return False
        return True

    def release_lock(self, lock_id):
        with self.lock:
            lock_obj = self.lock_map.get(lock_id)
            if lock_obj and lock_obj.status == "ACTIVE":
                lock_obj.status = "RELEASED"
                self.seat_manager.release(lock_obj.show_seat_ids)

    def expire_locks(self):
        with self.lock:
            for lock_id, lock_obj in list(self.lock.map.items()):
                if lock_obj.status == "ACTIVE" and lock_obj.expiry_time < time.time():
                    lock_obj.status = "EXPIRED"
                    self.seat_manager.release(lock_obj.show_seat_ids)


class PaymentManager:
    def process_payment(self, booking_id, payment_info):
        # Local stub: simulate always success
        return True


class BookingManager:

    def __init__(
        self,
        seat_manager: SeatManager,
        lock_manager: LockManager,
        payment_manager: PaymentManager,
    ):
        self.seat_manager = seat_manager
        self.lock_manager = lock_manager
        self.payment_manager = payment_manager
        self.bookings = {}

    def reserve_seats(self, user_id, show_id, seat_ids):
        show_seat_ids = [f"{show_id}_{sid}" for sid in seat_ids]
        lock_obj = self.lock_manager.acquire_lock(user_id, show_seat_ids)
        return lock_obj.lock_id, lock_obj.expiry_time

    def confirm_booking(self, lock_id, payment_info):
        if not self.lock_manager.validate_locks(lock_id):
            raise Exception("Lock invalid or expired")

        lock_obj = self.lock_manager.lock_map[lock_id]
        booking = Booking(lock_obj.user_id, lock_obj.show_seat_ids)
        success = self.payment_manager.process_payment(booking.booking_id, payment_info)
        if success:
            self.seat_manager.mark_as_booked(lock_obj.show_seat_ids)
            booking.status = "CONFIRMED"
            self.lock_manager.release_lock(lock_id)
        else:
            booking.status = "CANCELLED"
            self.lock_manager.release_lock(lock_id)

        self.bookings[booking.booking_id] = booking
        return booking


class ReconciliationManager:
    def __init__(self, lock_manager: LockManager):
        self.lock_manager = lock_manager

    def run_cleanup(self):
        self.lock_manager.expire_locks()


def try_reserve(user, booking_mgr, show_id, seat_ids):
    try:
        lock_id, expiry = booking_mgr.reserve_seats(user, show_id, seat_ids)
        print(f"[{user}] ✅ Lock acquired: {lock_id}, expires at {expiry}")
    except Exception as e:
        print(f"[{user}] ❌ Failed to reserve: {e}")


if __name__ == "__main__":
    seat_mgr = SeatManager()
    for seat_id in range(1, 4):  # 3 seats in show1
        seat_mgr.add_seat(ShowSeat(seat_id, "show1"))

    lock_mgr = LockManager(seat_mgr)
    payment_mgr = PaymentManager()
    booking_mgr = BookingManager(seat_mgr, lock_mgr, payment_mgr)
    reconciliation_mgr = ReconciliationManager(lock_mgr)

    # Two users trying for same seats at the same time
    t1 = threading.Thread(
        target=try_reserve, args=("user1", booking_mgr, "show1", [1, 2])
    )
    t2 = threading.Thread(
        target=try_reserve, args=("user2", booking_mgr, "show1", [1, 2])
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Check seat states
    for sid, seat in seat_mgr.seats.items():
        print(f"Seat {sid} → {seat.status}")


from enum import Enum


class VechileType(Enum):
    CAR = 1
    BUS = 2
    TWO_WHEELER = 3
    ELECTRIC_WHEELER = 4


class SLOT_TYPE(Enum):
    MEDIUM = 2
    SMALL = 1
    LARGE = 3


class Slot:
    def __init__(
        self,
        slotType: SLOT_TYPE,
        id,
        distance_from_entry: float,
        floor_number: int,
    ):
        self.slotType = slotType
        self.slot_id = id
        self.floor_number = floor_number
        self.distance_from_entry = distance_from_entry
        self.is_available = True
        self.lock = threading.Lock()

    def hold(self):
        with self.lock:
            if not self.is_available:
                raise Exception(f"Slot {self.slot_id} not available")
            self.is_available = True

    def relase(self):
        with self.lock:
            if not self.is_available:
                raise Exception(f"Slot {self.slot_id} available")
            self.is_available = False


class Vehicle:
    def __init__(self, vechile_number, vehicle_type: VechileType):
        vehicle_type = vehicle_type
        vechile_number = vechile_number


from abc import ABC, abstractmethod
import datetime


class Ticket:
    def __init__(
        self, ticket_id, starttime, endtime, amountPaid, vechile_type, vechilde_number
    ):
        self.ticket_id = ticket_id
        self.starttime = starttime
        self.endtime = endtime
        self.amountPaid = amountPaid
        self.vechile_type = vechile_type
        self.vechile_number = vechilde_number


rate_per_hour = {"CAR": 20, "BUS": 50, "TWO_WHEELER": 10, "ELECTRIC_WHEELER": 15}


class PricingStrategy:
    @abstractmethod
    def calculate_fee(
        self, entry_time: datetime.datetime, exit_time: datetime.datetime, vehicle_type
    ):
        pass


class HourlyPricing:
    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        hours = (exit_time - entry_time).seconds // 3600 + 1
        return rate_per_hour[vehicle_type] * hours


class FlatRatePricing:
    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        return 100 * rate_per_hour[vehicle_type]


class WeekendPricing(PricingStrategy):
    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        if entry_time.weekday() >= 5:
            return 50
        else:
            return 20


class PricingManager:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def calculate_fee(self, entry_time, exit_time, vehicle_type):
        return self.strategy.calculate_fee(entry_time, exit_time, vehicle_type)


class FloorManager:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.slot = []
        self.lock = threading.Lock()
    

    def add_slot(self):
        
