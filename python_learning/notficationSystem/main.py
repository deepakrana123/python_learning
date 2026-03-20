from queue.in_memory_queue import InMemoryQueue
from repository.notification_repo import NotificationRepository
from service.notfication_service import NotificationService
from worker.worker import Worker
from api.controller import NotificationController
from domain.models import ChannelType


queue = InMemoryQueue()
repo = NotificationRepository()
service = NotificationService()

worker = Worker(queue, service)
worker.start(5)


controller = NotificationController(queue)


controller.send_notification(
    {
        "id": "n1",
        "user_id": "u1",
        "template_id": "order",
        "channels": [ChannelType.SMS, ChannelType.EMAIL],
        "data": {},
    }
)
