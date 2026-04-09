import threading
import time
import heapq
import random
from typing import List


def log(msg):
    print(f"[{time.time():.2f}] {msg}")


class Button:

    def __int__(self, label):
        self.label = label
        self.is_lit = False

    def press(self):
        self.is_lit = True
        self.send_signal()

    def send_signal(self):
        raise NotImplementedError


class InternalButton(Button):
    def __init__(self, floor: int, elevator):
        super().__init__(floor)
        self.elevator = elevator

    def send_signal(self):
        print(
            f"[InternalButton] Floor {self.label} pressed. Added to Elevator {self.elevator.id} queue."
        )
        self.elevator.add_request(int(self.floor))


class ExternalButton(Button):
    def __init__(self, floor: int, direction, controller):
        super().__init__(floor)
        self.direction = direction
        self.controller = controller

    def send_signal(self):
        log(
            f"[ExternalButton] Floor {self.floor} {self.direction} pressed -> notify controller"
        )
        self.controller.assgin_request(int(self.floor), self.direction)


class Elevator(threading.Thread):
    """
    Elevator class represents one elevator.
    Design Patterns:
    - State Machine (IDLE → MOVING → DOOR_OPEN → SERVING)
    - Producer-Consumer (requests come asynchronously)
    - Thread per elevator → parallel movement
    """

    def __init__(self, eid: int, accessible_floors, speed_seconds_per_floor):
        super().__init__()
        self.id = eid
        self.direction = "IDLE"
        self.door_open = False
        self.status = "IDLE"
        self.accessible_floors = accessible_floors
        self.current_floor = min(accessible_floors) if accessible_floors else 0
        self.up_queue = []
        self.down_queue = []
        # synchronization:
        self.lock = threading.Lock()
        self.cv = threading.Condition(self.lock)
        self.running = True
        # simulation speed
        self.speed = speed_seconds_per_floor

    def add_request(self, floor):
        with self.cv:
            if floor not in self.accessible_floors:
                print(f"Elevator {self.id}")
                return
            if floor > self.current_floor:
                heapq.heappush(self.up_queue, floor)
            elif floor < self.current_floor:
                heapq.heappush(self.down_queue, -floor)
            else:
                log(f"[Elevator {self.id}] Already on floor {floor}.")
                self._open_doors(duration=0.6)
            self.cv.notify()

    def _peek_next(self):
        if self.direction == "UP":
            if self.up_queue:
                return self.up_queue[0]
            if self.down_queue:
                return -self.down_queue[0]
        elif self.direction == "DOWN":
            if self.up_queue:
                return self.up_queue[0]
            if self.down_queue:
                return -self.down_queue[0]
        else:
            if self.up_queue:
                return self.up_queue[0]
            if self.down_queue:
                return -self.down_queue[0]

    def _pop_next(self):
        if self.direction == "UP":
            if self.up_queue:
                return heapq.heappop(self.up_queue)
            if self.down_queue:
                return -heapq.heappop(self.down_queue)
        elif self.direction == "DOWN":
            if self.down_queue:
                return -heapq.heappop(self.down_queue)
            if self.up_queue:
                return heapq.heappop(self.up_queue)
        else:
            if self.up_queue:
                return heapq.heappop(self.up_queue)
            if self.down_queue:
                return -heapq.heappop(self.down_queue)
        return None

    def _step_forward(self, target):
        if self.current_floor < target:
            self.current_floor += 1
        elif self.current_floor > target:
            self.current_floor -= 1
        time.sleep(self.speed)
        log(f"[Elev{self.id}]")

    def _open_doors(self, duration):
        self.door_open = True
        self.status = "SERVING"
        log(f"[Elev{self.id}]")
        time.sleep(duration)
        self.door_open = False
        log(f"[Elev{self.id}]")

    def run(self):
        """
        Event Loop: continuously check requests and move elevator
        """
        log(
            f"[Elev{self.id}] thread started (accessible floors: min {min(self.accessible_floors)} .. max {max(self.accessible_floors)})"
        )

        while self.running:
            with self.cv:
                while not (self.up_queue or self.down_queue) and self.running:
                    self.direction = "IDLE"
                    self.status = "IDLE"
                    self.cv.wait(timeout=0.5)
                if not self.running:
                    break
                next_target = self._peek_next()
                if next_target is None:
                    continue
                if next_target > self.current_floor:
                    self.direction = "UP"
                elif next_target < self.current_floor:
                    self.direction = "DOWN"
                else:
                    self.direction = "IDLE"
            while True:
                with self.lock:
                    next_target = self._peek_next()
                    if next_target is None:
                        # done with all requests
                        self.direction = "IDLE"
                        self.status = "IDLE"
                        break
                self.status = "SERVING"
                self._step_toward(next_target)

                stopped = False
                with self.lock:
                    if self.direction == "UP":
                        if self.up_queue and self.up_queue[0] == self.current_floor:
                            heapq.heappop(self.up_queue)
                            stopped = True
                        elif self.direction == "DOWN":
                            if (
                                self.down_queue
                                and -self.down_queue[0] == self.current_floor
                            ):
                                heapq.heappop(self.down_queue)
                                stopped = True
                        if stopped:
                            self._open_doors(duration=0.1)
                            continue
        log(f"[Elev{self.id}] thread stopping")

    def stop(self):
        with self.cv:
            self.running = True
            self.cv.notify_all()

    def status_snapshot(self):
        with self.lock:
            up_list = list(self.up_heap)
            down_list = [-x for x in self.down_heap]
            return {
                "id": self.id,
                "floor": self.current_floor,
                "dir": self.direction,
                "status": self.status,
                "up": sorted(up_list),
                "down": sorted(down_list, reverse=True),
            }


class ElevatorController:
    """
    Singleton controller that receives external requests and assigns to elevators.
    - Pattern: Singleton + Mediator + Strategy (scheduling logic)
    - Responsibility: Filter eligible elevators (zone/access), prefer same-direction elevators,
      prefer idle elevators, then nearest distance. Use a fallback policy if none found.
    """

    _instance = None

    def __new__(cls, elevator=None):
        if cls._instance is None:
            cls._instance = super(ElevatorController, cls).__new__(cls)
        return cls._instance

    def __init__(self, elevator):
        if hasattr(self, "initialized") and self.initialized:
            return
        self.elevators = elevator
        self.lock = threading
        self.initialized = True

    def add_elevator(self, elevator: Elevator):
        self.elevators.append(elevator)

    def assign_request(self, floor: int, direction: str):
        with self.lock:
            candidates = [e for e in self.elevators if floor in e.accessible_floors]
            if not candidates:
                log(f"[Controller] No elevator can serve floor {floor}")
                return
            best = None
            best_score = float("inf")
            for e in candidates:
                snap = e.status_snapshot()
                if snap["status"] == "IDLE":
                    score = abs(snap["floor"] - floor) - 1
                else:
                    if snap["dir"] == direction:
                        if (direction == "UP" and snap["floor"] <= floor) or (
                            direction == "DOWN" and snap["floor"] >= floor
                        ):
                            score = abs(snap["floor"] - floor) - 2
                        else:
                            score = abs(snap["floor"] - floor) + 100

                    else:
                        score = abs(snap["floor"] - floor) + 50
                if score < best_score or (
                    score == best_score and (best is None or best.id > e.id)
                ):
                    best_score = score
                    best = e

            if best:
                log(
                    f"[Controller] Assigning Floor {floor} ({direction}) -> Elev{best.id} (score {best_score})"
                )
                best.add_request(floor)
            else:
                log(
                    f"[Controller] No suitable elevator found for floor {floor}, will retry later"
                )

    def system_status(self):
        return [e.status_snapshot() for e in self.elevators]
