import time
from datetime import datetime
import threading


class BatchBuffer:
    def __init__(self, batch_size, flush_interval, flush_callback):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.flush_callback = flush_callback
        self.batch = []
        self.lock = threading.Lock()
        self.last_flush_time = datetime.now()
        self._start_background_thread()

    def add(self, item):
        with self.lock:
            self.batch.append(item)
            if len(self.batch) >= self.batch_size:
                self._flush()

    def _flush(self):
        if not self.batch:
            return []
        batch_to_send = self.batch
        self.batch = []
        self.last_flush_time = datetime.now()
        self.flush_callback(batch_to_send)

    def _run_background_task(self):
        while True:
            time.sleep(0.5)
            with self.lock:
                if (
                    self.batch
                    and datetime.now() - self.last_flush_time >= self.flush_interval
                ):
                    self._flush()

    def _start_background_thread(self):
        t = threading.Thread(target=self._run_background_task, args=("job1"))
        t.start()
