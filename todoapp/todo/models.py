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
    created_at = models.DateTimeField(auto_now_add=True, )
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.PENDING
    )

    @classmethod
    def _serialize_tasks(cls, tasks):
        return [cls._serialize_task(task) for task in tasks]

    @classmethod
    def _serialize_task(cls, task):
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "status": task.status,
        }

    @classmethod
    def create(cls, data):
        new_task = cls.objects.create(
            title=data["title"],
            description=data["description"],
            status=data["status"]
        )
        return cls._serialize_task(new_task)

    @classmethod
    def get_by_id(cls, task_id):
        task = cls.objects.get(id=task_id)
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": task.created_at,
            "status": task.status,
        }

    @classmethod
    def get_all(cls):
        tasks = cls.objects.all()
        return cls._serialize_tasks(tasks)

    @classmethod
    def complete_task(cls, tasks_ids):
        tasks = cls.objects.filter(id__in=tasks_ids)
        tasks.update(status=Task.Status.DONE)
        return cls._serialize_tasks(tasks)

    @classmethod
    def get_filtered(cls, date_from, date_to, title):
        tasks = cls.objects.all()
        if date_from:
            tasks = tasks.filter(created_at__gte=date_from)
        if date_to:
            tasks = tasks.filter(created_at__lte=date_to)
        if title:
            tasks = tasks.filter(title__icontains=title)
        return cls._serialize_tasks(tasks)