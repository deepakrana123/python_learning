# IDLE->REQUESTING->WAITING->RETRYING → (SUCCESS | FAILED)
# FSM = (state + events + transitions)


import time
import random
import threading


class RetryFSM:
    def __init__(self, max_retry, base_delay, snm):
        self.state = "IDLE"
        self.retries = 0
        self.max_retry = max_retry
        self.base_delay = base_delay
        self.snm = snm

    def make_request(self):
        return random.random() > 0.7

    def run(self):
        self.state = "REQUESTING"

        while True:
            print(f"State->{self.state} {self.snm}")

            if self.state == "REQUESTING":
                success = self.make_request()
                print(success, "hi")
                if success:
                    self.state = "SUCCESS"
                else:
                    self.state = "WAITING"
            elif self.state == "WAITING":
                if self.retries >= self.max_retry:
                    self.state = "FAILED"
                else:
                    self.state = "RETRYING"
            elif self.state == "RETRYING":
                self.retries += 1
                jitter = random.uniform(0, 0.5)
                delay = self.base_delay + jitter
                # delay = self.base_delay
                print(f"sleep retry #{self.retries} {delay}")
                time.sleep(delay)
                self.state = "REQUESTING"
            elif self.state == "SUCCESS":
                print("Request succeeded")
                break
            elif self.state == "FAILED":
                print("Request failed")
                break


# fsms = [RetryFSM(3, 2, f"FSM{i}") for i in range(5)]
# threads = [threading.Thread(target=f.run) for f in fsms]

# for t in threads:
#     t.start()
# for t in threads:
#     t.join()


class HeartbeatFSM:
    def __init__(self, interval=0.1, max_missed=3):
        self.state = "ALIVE"
        self.interval = interval
        self.max_missed = max_missed
        self.missed = 0

    def receive_heartbeat(self):
        return random.random() < 0.7

    def run(self, cycles=10):
        for _ in range(cycles):
            print(f"State -> {self.state}")
            got_heartbeat = self.receive_heartbeat()

            if got_heartbeat:
                print("Heartbeat received")
                self.missed = 0
                self.state = "ACTIVE"
            else:
                print("Heart missed")
                self.missed += 1
                if self.missed == 1:
                    self.state = "MISSED"
                elif self.missed < self.max_missed:
                    self.state = "SUSPECT"
                else:
                    self.state = "DEAD"
                    print("Node declared dead")
                    break
        time.sleep(self.interval)
