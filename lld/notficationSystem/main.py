from lld.notficationSystem.queue.in_memory_queue import InMemoryQueue
from lld.notficationSystem.repository.notification_repo import NotificationRepository
from service.notfication_service import NotificationService
from lld.notficationSystem.worker.worker import Worker
from lld.notficationSystem.api.controller import NotificationController
from lld.notficationSystem.domain.models import ChannelType
from Scheduler import Scheduler


queue = InMemoryQueue()
repo = NotificationRepository()
service = NotificationService()

worker = Worker(queue, service)
worker.start(5)


controller = NotificationController(queue)
scheduler = Scheduler(controller)


controller.send_notification(
    {
        "id": "n1",
        "user_id": "u1",
        "template_id": "order",
        "channels": [ChannelType.SMS, ChannelType.EMAIL],
        "data": {},
    }
)

scheduler.add_job(
    {
        "job_id": "reminder_1",
        "event_type": "REMINDER",
        "interval": 10,
        "payload": {"user_id": "u1", "data": {"msg": "Daily reminder"}},
    }
)

scheduler.start()
