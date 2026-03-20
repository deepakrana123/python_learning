import threading


class Worker:
    def __init__(self, queue, service):
        self.queue = queue
        self.service = service

    def start(self, num_threads=3):
        for _ in range(num_threads):
            t = threading.Thread(target=self.run, daemon=True)
            t.start()

    def run(self):
        while True:
            task = self.queue.pull()
            success = self.service.process()

            if not success:
                self.handle_failure(task)

    def handle_failure(self, task):
        task["attempt"] += 1
        if task["attempt"] < 3:
            self.queue.push(task)

        else:
            task["channel_index"] += 1
            task["attempt"] = 0
            self.queue.push(task)
