import datetime
import threading
import uuid
from datetime import datetime,timedelta,time

class Scheduler:
    def __init__(self, controller):
        self.jobs = []
        self.controller = controller
        self.running = True
        self.thread =None

    def add_job(self, job):
        if "next_run" not in job:
            job["next_run"]=datetime.now()
        self.jobs.append(job)
    

    def start(self):
        self.running=True
        self.thread=threading.Thread(target=self.run)
        self.thread.start()
    
    def stop(self):
        self.running=False
        if self.thread:
            self.thread.join()
    
    def run(self):
        while self.running:
            now=datetime.now()
            for job in self.jobs:
                if job["next_run"]<=now:
                    self.trigger(job)
                    job["next_run"] = job["next_run"] + timedelta(seconds=job["interval"])
            time.sleep()
    def trigger(self,job):
        event = {
            "id": str(uuid.uuid4()),
            "event_type": job["event_type"],
            "user_id": job["payload"]["user_id"],
            "data": job["payload"].get("data", {}),
        }
        self.controller.send_event(event)

