# api/controller.py

from domain.models import Notification


class NotificationController:

    def __init__(self, queue):
        self.queue = queue

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
