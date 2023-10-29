# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from todo.models import TodoItem
from django.utils import timezone

class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse('home')

        self.task1=TodoItem.objects.create(title='task1',completed=False,created_at=timezone.now())
        self.task2=TodoItem.objects.create(title='task2',completed=True,created_at=timezone.now())
        self.task3=TodoItem.objects.create(title='task3',completed=False,created_at=timezone.now())

    def test_home_view(self):
        response = self.client.get(self.url)

         # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is used
        self.assertTemplateUsed(response, 'home.html')

        # Assert that the response contains the tasks
        self.assertIn('tasks', response.context)
        self.assertIn(self.task1, response.context['tasks'])
        self.assertIn(self.task3, response.context['tasks'])

        # Assert that the response contains the completed task
        self.assertIn('completed_tasks', response.context)
        self.assertIn(self.task2, response.context['completed_tasks'])


class AddTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
    
    def add_task_success(self):
        url = reverse('add_task')
        data = {'title': 'Test task'}
        response = self.client.post(url, data)
        # check if the view redirects
        self.assertEqual(response.status_code, 302)
        # check if no task was created
        self.assertEqual(TodoItem.objects.count(), 1)
        
    def add_task_blank(self):
        url = reverse('add_task')
        data = {'title': ''}
        response = self.client.post(url, data)
        # check if the view redirects
        self.assertEqual(response.status_code, 302)
        # check if no task was created
        self.assertEqual(TodoItem.objects.count(), 0)
        messages = list(response.wsgi_request._messages)
        # chek if an error message was added
        self.assertEqual(len(messages), 1)
        # Check the error message content
        self.assertEqual(str(messages[0]), 'Task cannot be blank.')



class MarkAsDoneViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.task = TodoItem.objects.create(title='Task test', completed=False)

    def test_mark_as_done(self):
        url = reverse('mark_as_done', args=[self.task.id])
        response = self.client.get(url)
        # check if view redirects
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        # Check if the task is marked as completed
        self.assertTrue(self.task.completed)
    
    def test_mark_as_done_invalid_task(self):
        invalid_pk = 999
        url = reverse('mark_as_done', args=[invalid_pk])
        response = self.client.get(url)
        # Check if a 404 response is returned
        self.assertEqual(response.status_code, 404)
        # Check if the task state is unchanged
        self.task.refresh_from_db()
        # Ensure the task is still marked as not completed
        self.assertFalse(self.task.completed)


class MarkAsUndoneViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.task = TodoItem.objects.create(title='Test Task', completed=True)

    def test_mark_as_undone(self):
        url = reverse('mark_as_undone', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Check if the view redirects
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)  # Check if the task is marked as completed
    
    def test_mark_as_undone_invalid_task(self):
        invalid_pk = 999  # Assuming this PK does not exist
        url = reverse('mark_as_undone', args=[invalid_pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Check if a 404 response is returned


class EditTaskViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.task = TodoItem.objects.create(title='Task test')
    
    def edit_task_success(self):
        url = reverse('edit_task', args=[self.task.id])
        data = {'title': 'New Task'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        # Check if the task was updated
        self.assertEqual(self.task.title, 'New Task')
    
    def edit_task_blank(self):
        url = reverse('edit_task', args=[self.task.id])
        data = {'title': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        # check if the task remains unchanged
        self.assertEqual(self.task.title, 'Test Task')
        # Check if an error message was added
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Task cannot be blank.')
    
    def test_edit_task_invalid_task(self):
        invalid_pk = 999  # Assuming this PK does not exist
        url = reverse('edit_task', args=[invalid_pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Check if a 404 response is returned

        # Optional: Check if the task state is unchanged
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Task test')

    def test_edit_task_get_request(self):
        url = reverse('edit_task', args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_task.html')
        self.assertIn('get_task', response.context)
        self.assertEqual(response.context['get_task'], self.task)


class DeleteTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.task = TodoItem.objects.create(title='Test Task')

    def test_delete_task_confirmed(self):
        url = reverse('delete_task', args=[self.task.id])
        data = {'confirmed': 'true'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Check if the view redirects
        self.assertFalse(TodoItem.objects.filter(pk=self.task.id).exists())  # Check if the task was deleted

    def test_delete_task_invalid_task(self):
        invalid_pk = 999  # Assuming this PK does not exist
        url = reverse('delete_task', args=[invalid_pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Check if a 404 response is returned

    
class TaskModelTest(TestCase):

    def test_task_model_str(self):
        task = TodoItem.objects.create(title='Test Task')
        self.assertEqual(str(task), 'Test Task')
    
    def test_task_model_defaults(self):
        task = TodoItem.objects.create(title='Test Task')
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)
    
    def task_update(self):
        task = TodoItem.objects.create(title='Test Task')
        task.title = 'Updated Task'
        task.save()
        updated_task = TodoItem.objects.get(id=task.id)
        self.assertEqual(updated_task.task, 'Updated Task')

