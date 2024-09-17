from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEN", "Pending"
        IN_PROGRESS = "PRO", "In Progress"
        DONE = "DON", "Done"
        CANCELLED = "CAN", "Cancelled"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.PENDING
    )

    @classmethod
    def create(cls, data):
        return cls.objects.create(
            title=data["title"],
            description=data["description"],
            status=data["status"]
        )

    @classmethod
    def get_by_id(cls, task_id):
        task = cls.objects.get(id=task_id)
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        }

    @classmethod
    def get_all(cls):
        tasks = cls.objects.all()
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
            }
            for task in tasks
        ]