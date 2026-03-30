# api/controller.py

from domain.models import Notification
from ..rule_engine.rule_engine import ActionMapper
from ..rule_engine.rule_engine import Event


class NotificationController:
    def __init__(self, queue, rule_engine):
        self.queue = queue
        self.rule_engine = rule_engine

    def send_notification(self, request):
        notification = Notification(
            request["id"],
            request["user_id"],
            request["template_id"],
            request["channels"],
            request["data"],
        )

        task = {"notification": notification, "channel_index": 0, "attempt": 0}

        self.queue.push(task)

        return {"status": "accepted"}

    def send_event(self, request):

        notification = Event(event_type=request["event_type"], payload=request["data"])
        mapper = ActionMapper()
        actions = self.rule_engine.process(notification)
        for tasks in actions:
            notfication = mapper.to_notification(tasks)
            task = {
                "notification": notfication,
                "channel_index": 0,
                "attempt": 0,
            }
            self.queue.push(task)
