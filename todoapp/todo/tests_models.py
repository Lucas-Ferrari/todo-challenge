from django.test import TestCase
from todo.models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        """Create various tasks for testings"""
        data = {
            "title": "test title",
            "description": "test description for a task",
            "status": "PEN",
        }

        for i in range(0, 5):
            ts_create = data
            ts_create['title'] = data['title'] + str(i)
            Task.create(data)

        data_2 = {
            "title": "filter title",
            "description": "test description for a filtered task",
            "status": Task.Status.IN_PROGRESS
        }
        Task.create(data_2)

    def test_create(self):
        data = {
            "title": "test title",
            "description": "test description for a task",
            "status": "PEN"
            }
        task = Task.create(data)

        self.assertIsNotNone(task)

        task_db = Task.objects.last()

        self.assertIsInstance(task_db, Task)
        self.assertEqual(task_db.title, task["title"])
        self.assertEqual(task_db.description, task["description"])
        self.assertEqual(task_db.status, Task.Status.PENDING)

    def test_get_by_id(self):
        task_db = Task.get_by_id(2)

        self.assertIsInstance(task_db, dict)
        self.assertEqual(task_db['id'], 2)

    def test_get_by_id_not_found(self):
        task_db = Task.get_by_id(200000000)

        self.assertIsNone(task_db)

    def test_get_all(self):
        tasks_db = Task.get_all()

        self.assertEqual(len(tasks_db), 6)

    def test_complete_task(self):
        task_db = Task.objects.first()

        self.assertEqual(task_db.status, Task.Status.PENDING)

        tasksid_list = [task_db.id]

        updated_tasks = Task.complete_task(tasks_ids=tasksid_list)

        self.assertEqual(len(updated_tasks), 1)

        task_db.refresh_from_db()
        self.assertEqual(task_db.status, Task.Status.DONE)

    def test_get_filtered(self):
        filtered_tasks = Task.get_filtered(
            date_from=None, date_to=None, title="filter title"
        )

        self.assertIsInstance(filtered_tasks, list)
        self.assertEqual(len(filtered_tasks), 1)

        task = filtered_tasks[0]
        self.assertEqual(task['title'], "filter title")
        self.assertEqual(task["description"], "test description for a filtered task")
        self.assertEqual(task["status"], Task.Status.IN_PROGRESS)
