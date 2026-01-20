from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Label


class LabelCRUDTest(TestCase):
    fixtures = ['labels.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='testuser')
        self.client.login(username='testuser', password='testpass')
        self.label = Label.objects.get(pk=1)

    def test_label_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('labels:label_list'))
        self.assertRedirects(response, '/login/?next=/labels/')

    def test_label_list_authenticated(self):
        response = self.client.get(reverse('labels:label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertContains(response, 'Баг')

    def test_label_create(self):
        data = {'name': 'Документация'}
        response = self.client.post(reverse('labels:label_create'), data)
        self.assertRedirects(response, reverse('labels:label_list'))
        self.assertTrue(Label.objects.filter(name='Документация').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно создана')

    def test_label_update(self):
        data = {'name': 'Ошибка'}
        response = self.client.post(reverse('labels:label_update', kwargs={'pk': self.label.pk}), data)
        self.assertRedirects(response, reverse('labels:label_list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Ошибка')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно обновлена')

    def test_label_delete_success(self):
        response = self.client.post(reverse('labels:label_delete', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('labels:label_list'))
        self.assertFalse(Label.objects.filter(pk=2).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')

    def test_label_delete_protected(self):
        response = self.client.post(reverse('labels:label_delete', kwargs={'pk': self.label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assertTemplateUsed(response, 'labels/label_confirm_delete.html')
        self.assertContains(response, 'Метку нельзя удалить, потому что она используется в задаче')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метку нельзя удалить, потому что она используется в задаче')
