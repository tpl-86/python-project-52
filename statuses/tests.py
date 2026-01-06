from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Status


class StatusCRUDTest(TestCase):
    fixtures = ['statuses.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='testuser')
        self.client.login(username='testuser', password='testpass')  # Логин тестового пользователя
        self.status = Status.objects.get(pk=1)  # Существующий статус из фикстур

    def test_status_list_unauthenticated(self):
        self.client.logout()  # Разлогин
        response = self.client.get(reverse('statuses:status_list'))
        self.assertRedirects(response, '/login/?next=/statuses/')  # Редирект на login

    def test_status_list_authenticated(self):
        response = self.client.get(reverse('statuses:status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertContains(response, 'Новый')  # Проверяет наличие статуса

    def test_status_create(self):
        data = {'name': 'На тестировании'}
        response = self.client.post(reverse('statuses:status_create'), data)
        self.assertRedirects(response, reverse('statuses:status_list'))
        self.assertTrue(Status.objects.filter(name='На тестировании').exists())
        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_status_update(self):
        data = {'name': 'Завершен'}
        response = self.client.post(reverse('statuses:status_update', kwargs={'pk': self.status.pk}), data)
        self.assertRedirects(response, reverse('statuses:status_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Завершен')
        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

    def test_status_delete_success(self):
        # Удаляем статус, который НЕ используется (pk=2 из фикстур)
        response = self.client.post(reverse('statuses:status_delete', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('statuses:status_list'))
        self.assertFalse(Status.objects.filter(pk=2).exists())
        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')

    def test_status_delete_protected(self):
        # Удаляем статус, который используется в задаче (pk=1 из фикстур)
        response = self.client.post(reverse('statuses:status_delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 200)  # Остаётся на странице delete с ошибкой (из-за get() в post)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())  # Не удалён
        self.assertTemplateUsed(response, 'statuses/status_confirm_delete.html')
        # Проверка сообщения об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус нельзя удалить, потому что он используется')
