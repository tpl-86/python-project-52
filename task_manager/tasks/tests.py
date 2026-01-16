from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Task
from django.contrib.auth.models import User
from statuses.models import Status
from labels.models import Label

class TaskCRUDTest(TestCase):
    fixtures = ['tasks.json']

    def setUp(self):
        self.client = Client()
        self.author = User.objects.get(username='author')
        self.other = User.objects.get(username='other')
        self.client.login(username='author', password='testpass')
        self.task = Task.objects.get(pk=1)

    def test_task_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:task_list'))
        self.assertRedirects(response, '/login/?next=/tasks/')

    def test_task_list_authenticated(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Тестовая задача')

    def test_task_create(self):
        data = {
            'name': 'Новая задача',
            'description': 'Описание',
            'status': 1,
            'executor': 2
        }
        response = self.client.post(reverse('tasks:task_create'), data)
        self.assertRedirects(response, reverse('tasks:task_list'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

    def test_task_update(self):
        data = {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': 1,
            'executor': 2
        }
        response = self.client.post(reverse('tasks:task_update', kwargs={'pk': self.task.pk}), data)
        self.assertRedirects(response, reverse('tasks:task_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

    def test_task_delete_by_author(self):
        # Создаём новую задачу без связей для удаления
        new_task = Task.objects.create(name='Удаляемая', status=Status.objects.get(pk=1), author=self.author)
        response = self.client.post(reverse('tasks:task_delete', kwargs={'pk': new_task.pk}))
        self.assertRedirects(response, reverse('tasks:task_list'))
        self.assertFalse(Task.objects.filter(pk=new_task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

    def test_task_delete_by_non_author(self):
        self.client.logout()
        self.client.login(username='other', password='testpass')  # Логин под другим пользователем
        response = self.client.post(reverse('tasks:task_delete', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 403)  # Или редирект, в зависимости от handle_no_permission
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())  # Не удалена
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения другого пользователя.')

    def test_task_detail(self):
        response = self.client.get(reverse('tasks:task_detail', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'Тестовая задача')

class TaskFilterTest(TestCase):
    fixtures = ['tasks.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='author')
        self.client.login(username='author', password='testpass')
        self.status = Status.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.task = Task.objects.get(pk=1)  # Добавлено: теперь self.task определён

    def test_filter_by_status(self):
        response = self.client.get(reverse('tasks:task_list'), {'status': self.status.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')

    def test_filter_by_executor(self):
        Task.objects.create(name='Задача с исполнителем', status=self.status, author=self.user, executor=self.other_user)
        response = self.client.get(reverse('tasks:task_list'), {'executor': self.other_user.pk})
        self.assertContains(response, 'Задача с исполнителем')

    def test_filter_by_label(self):
        # Создаём метку и связываем с задачей динамически
        label = Label.objects.create(name='Тестовая метка')
        self.task.labels.add(label)
        response = self.client.get(reverse('tasks:task_list'), {'labels': label.pk})
        self.assertContains(response, 'Тестовая задача')

    def test_filter_self_tasks(self):
        response = self.client.get(reverse('tasks:task_list'), {'self_tasks': 'on'})
        self.assertContains(response, 'Тестовая задача')

    def test_filter_combined(self):
        response = self.client.get(reverse('tasks:task_list'), {'status': self.status.pk, 'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
