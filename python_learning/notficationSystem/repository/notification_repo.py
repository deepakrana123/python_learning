class NotificationRepository:
    def __init__(self):
        self.store = {}

    def exists(self, notification_id: str):
        return notification_id in self.store

    def save(self, notification_id: str):
        self.store[notification_id] = "SENT"
