import json
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from todo.models import Task

class TaskListTestCase(APITestCase):
    def setUp(self):
        """
        Create the client to test the views and a user to authenticate
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username="user_test", password="pwd_test")

        data = {
            "title": "test title",
            "description": "test description for a task",
            "status": "PEN",
        }

        for i in range(0, 5):
            ts_create = data
            ts_create["title"] = data["title"] + str(i)
            Task.create(data)

        data_2 = {
            "title": "filter title",
            "description": "test description for a filtered task",
            "status": Task.Status.IN_PROGRESS,
        }
        Task.create(data_2)

    def test_get_all_tasks(self):
        """
        Test the get all tasks view
        """
        url = reverse("tasks_list")
        self.client.force_authenticate(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 6)

    def test_get_all_tasks_401(self):
        """
        Test the get all tasks view without authentication
        """
        url = reverse("tasks_list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_filtered_tasks(self):
        """
        Test the get filtered tasks view
        """
        data = {"title": "filter title"}
        url = reverse("tasks_list")

        self.client.force_authenticate(self.user)
        #Using generic to enable sending data on get
        response = self.client.generic(
            method="GET",
            path=url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["title"], data["title"])

    def test_get_filtered_tasks_401(self):
        """
        Test the get filtered tasks view without authentication
        """
        data = {"title": "filter title"}
        url = reverse("tasks_list")

        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 401)


class TaskViewTestCase(APITestCase):

    def setUp(self):
        """
        Create the client to test the views and a user to authenticate
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username="user_test", password="pwd_test")

        data = {
            "title": "test title",
            "description": "test description for a task",
            "status": "PEN",
        }

        for i in range(0, 5):
            ts_create = data
            ts_create["title"] = data["title"] + str(i)
            Task.create(data)

        data_2 = {
            "title": "filter title",
            "description": "test description for a filtered task",
            "status": Task.Status.IN_PROGRESS,
        }
        Task.create(data_2)

    def test_get_task_by_id(self):
        """
        Test the get task by id view
        """
        data = {"id": 3}
        url = reverse("tasks_get_by_id")

        self.client.force_authenticate(self.user)

        response = self.client.generic(
            method="GET",
            path=url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["id"], data["id"])

    def test_get_task_by_id_401(self):
        """
        Test the get task by id view without authentication
        """
        data = {"id": 3}
        url = reverse("tasks_get_by_id")

        response = self.client.generic(
            method="GET",
            path=url,
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_create_task(self):
        """
        Test create a new task
        """
        data = {
            "title": "new title",
            "description": "new description",
            "status": Task.Status.IN_PROGRESS,
        }
        url = reverse("tasks_create")

        self.client.force_authenticate(self.user)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["status"], data["status"])

        # Verify what we got on the database
        task = Task.get_by_id(response.data["id"])
        self.assertEqual(task['title'], data["title"])
        self.assertEqual(task['description'], data["description"])
        self.assertEqual(task['status'], data["status"])

    def test_create_task_401(self):
        """
        Test create a new task without authentication
        """
        data = {
            "title": "new title",
            "description": "new description",
            "status": Task.Status.IN_PROGRESS,
        }
        url = reverse("tasks_create")

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 401)

    def test_set_complete(self):
        """
        Test set a list of tasks as complete
        """
        data = [1, 2, 3]
        url = reverse("tasks_complete")

        self.client.force_authenticate(self.user)

        response = self.client.put(url, json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

        for task in response.data:
            self.assertEqual(task["status"], Task.Status.DONE)
