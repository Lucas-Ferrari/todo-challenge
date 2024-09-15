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