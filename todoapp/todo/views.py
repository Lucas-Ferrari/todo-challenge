from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from todo.models import Task

class TaskList(APIView):
    """
    have to accept no params or datefrom and date to to filter the tasks
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Get filtered tasks
        """
        if request.data == {}:
            return Response(Task.get_all())

        date_from = request.data.get('datefrom', None)
        date_to = request.data.get('dateto', None)
        title = request.data.get('title', None)
        tasks = Task.get_filtered(date_from, date_to, title)

        return Response(tasks)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Get task by id
        """
        task_id = request.data.get('id', 0)
        if task_id:
            task = Task.get_by_id(task_id=task_id)
            return Response(task)
        content = {"error": "Task id {task_id} not found"}
        return Response(content)

    def post(self, request):
        """
        Create a new task.
        request.data should be a dictionary with the following keys:
        {title: str, description: str, status: str}
        """
        assert isinstance(request.data, dict) # move into a serializer
        task = Task.create(request.data)
        return Response(task, status=201)

    def put(self, request):
        """
        Sets a list of tasks as completed status.
        request.data should be a list with the following format:
        [task_id_1, task_id_2, ..., task_id_n]
        returns a list of tasks with the updated status
        """
        assert isinstance(request.data, list) # move into a serializer
        tasks = Task.complete_task(request.data)
        return Response(tasks)
