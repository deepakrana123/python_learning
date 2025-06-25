from abc import ABC, abstractmethod
import time
import threading

# Command Pattern separates what triggers an action (like a button) from how the action is done (like going to a floor), by turning the action into an object.


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class GoToFloorCommand(Command):
    def __init__(self, floor: int):
        self.floor = floor

    def execute(self):
        print("f[command] request")
        return super().execute()


class EmergencyStopCommand(Command):
    def execute(self):
        print("f[command] request")
        return super().execute()


class OpenDoorCommand(Command):
    def execute(self):
        print("f[command] request")
        return super().execute()


class EmergencyStopCommand(Command):
    def execute(self):
        print("f[command] request")
        return super().execute()


class CloseDoorCommand(Command):
    def execute(self):
        print("f[command] request")
        return super().execute()


class FireUnlockCommand(Command):
    def execute(self):
        print("f[command] request")
        return super().execute()


class Button:
    def __init__(self, label: str, command: Command):
        self.label = label
        self.command = command

    def press(self):
        self.command.execute()


class ButtonFactory:
    @staticmethod  # meas can call without self and cls as this is not part of inheritance system
    def create_button(config: dict, user_role: str):
        label = config["label"]
        restricted_to = config.get("restricted_To", [])

        if restricted_to and user_role not in restricted_to:
            raise PermissionError(
                f"Role '{user_role}' is not allowed to access button '{label}'"
            )
        if config["type"] == "floor":
            command = GoToFloorCommand(int(label))
        elif config["type"] == "open":
            command = OpenDoorCommand()
        elif config["type"] == "fire_unlock":
            command = FireUnlockCommand()
        else:
            raise ValueError(f"Unsupported button type: {config['type']}")

        return Button(label, command)


class ElevatorState(ABC):
    @abstractmethod
    def handle_command(self, elevate, command):
        pass


class IdleState(ElevatorState):
    def handle_command(self, elevator, command):
        if isinstance(command, GoToFloorCommand):
            print(
                f"Elevator moving from floor {elevator.current_floor} to {command.floor}"
            )
            elevator.current_floor = command.floor
            elevator.set_state(DoorsOpenState())
        elif isinstance(command, OpenDoorCommand):
            print("Doors opening...")
            elevator.set_state(DoorsOpenState())
        elif isinstance(command, EmergencyStopCommand):
            print("Emergency stop activated!")
            elevator.set_state(EmergencyStopState())


class DoorsOpenState(ElevatorState):
    def handle_command(self, elevate, command):
        return super().handle_command(elevate, command)


class EmergencyStopState(ElevatorState):
    def handle_command(self, elevate, command):
        return super().handle_command(elevate, command)


class Elevator:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.state = IdleState()
        self.lock = threading.Lock()
        self.up_queue = []
        self.down_queue = []
        self.direction = None
        self.lock = threading.lock()

    def set_state(self, new_state):
        self.state = new_state

    def handle_command(self, command):
        self.state.handle_command(self, command)

    # def move_to_floor(self, target_floor):
    #     if target_floor == self.current_floor:
    #         print(f"Already on floor {self.current_floor}")
    #         return
    #     direction = 1 if target_floor > self.current_floor else -1
    #     while self.current_floor != target_floor:
    #         self.current_floor += direction
    #         print(f"Moving... Floor {self.current_floor}")
    #         time.sleep(0.5)  # Simulates delay per floor

    def add_request(self, floor):
        with self.lock:
            if self.current_floor > floor:
                if floor not in self.up_queue:
                    self.up_queue.append(floor)
                    self.up_queue.sort()
                elif floor < self.current_floor:
                    if floor not in self.up_queue:
                        self.up_queue.append(floor)
                        self.up_queue.sort()
                else:
                    print(f"Already on floor {floor}")
                    return
        if self.direction is None:
            self.direction = "up" if floor > self.current_floor else "down"
            thread = threading.Thread(target=self.process_requests)
            thread.start()
            # self.process_requests()

    def process_requests(self):
        while self.up_queue or self.down_queue:
            with self.lock:
                if self.direction == "up" and self.up_queue:
                    next_floor = self.up_queue.pop(0)
                elif self.direction == "down" and self.down_queue:
                    next_floor = self.down_queue.pop(0)
                else:
                    if self.direction == "up" and self.down_queue:
                        self.direction = "down"
                        continue
                    elif self.direction == "down" and self.up_queue:
                        self.direction = "up"
                        continue
                    else:
                        self.direction = None
                        break
                self.move_to_floor(next_floor)

        self.set_state(IdleState())

    def move_to_floor(self, target_floor):
        direction = 1 if target_floor > self.current_floor else -1
        while self.current_floor != target_floor:
            self.current_floor += direction
            print(f"Elevator {self.id} moving... Floor {self.current_floor}")
            time.sleep(0.5)
        print(f"Elevator {self.id} arrived at floor {self.current_floor}")
        self.set_state(DoorsOpenState())
        time.sleep(1)
        self.set_state(IdleState())


class ButtonPanelFactory(ABC):
    @abstractmethod
    def create_floor_button(self, floor):
        pass

    @abstractmethod
    def create_door_button(self):
        pass

    @abstractmethod
    def create_emergency_button(self):
        pass


class RegularPanelFactory(ButtonPanelFactory):
    def create_floor_button(self, floor):
        return Button(str(floor), GoToFloorCommand(floor))

    def create_door_button(self):
        return Button("Open", OpenDoorCommand())

    def create_emergency_button(self):
        return Button("Emergency", EmergencyStopCommand())


class ElevatorManager:
    def __init__(self, elevators):
        self.elevators = elevators

    def request_elevator(self, floor):
        best = self.select_best_elevator(floor)
        if best:
            print(f"Assigning elevator {best.id} to floor {floor}")
            best.add_request(floor)

    def select_best_elevator(self, floor):
        # Simple nearest elevator selection
        available = [
            e
            for e in self.elevators
            if e.direction is None or e.state.__class__ == IdleState
        ]
        if not available:
            return None
        return min(available, key=lambda e: abs(e.current_floor - floor))


# ---------------------- Demo ---------------------- #
# Demonstrates a multi-elevator system using Command, State, Abstract Factory, and Manager patterns.


def run_demo():
    elevators = [Elevator(id=i) for i in range(2)]
    manager = ElevatorManager(elevators)
    factory = RegularPanelFactory()

    btn1 = factory.create_floor_button(5)
    btn2 = factory.create_floor_button(1)
    btn3 = factory.create_floor_button(12)

    btn1.press(manager.select_best_elevator(5))
    btn2.press(manager.select_best_elevator(1))
    btn3.press(manager.select_best_elevator(12))


# Uncomment to run:
# run_demo()
