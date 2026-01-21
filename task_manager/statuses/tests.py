from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    fixtures = ["statuses.json"]

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="testuser")
        self.client.login(username="testuser", password="testpass")
        self.status = Status.objects.get(pk=1)

    def test_status_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("statuses:status_list"))
        self.assertRedirects(response, "/login/?next=/statuses/")

    def test_status_list_authenticated(self):
        response = self.client.get(reverse("statuses:status_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/status_list.html")
        self.assertContains(response, "Новый")

    def test_status_create(self):
        data = {"name": "На тестировании"}
        response = self.client.post(reverse("statuses:status_create"), data)
        self.assertRedirects(response, reverse("statuses:status_list"))
        self.assertTrue(Status.objects.filter(name="На тестировании").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно создан")

    def test_status_update(self):
        data = {"name": "Завершен"}
        response = self.client.post(
            reverse("statuses:status_update", kwargs={"pk": self.status.pk}),
            data,
        )
        self.assertRedirects(response, reverse("statuses:status_list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Завершен")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно изменен")

    def test_status_delete_success(self):
        response = self.client.post(
            reverse("statuses:status_delete", kwargs={"pk": 2})
        )
        self.assertRedirects(response, reverse("statuses:status_list"))
        self.assertFalse(Status.objects.filter(pk=2).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно удален")

    def test_status_delete_protected(self):
        response = self.client.post(
            reverse("statuses:status_delete", kwargs={"pk": self.status.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        self.assertTemplateUsed(response, "statuses/status_confirm_delete.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Статус нельзя удалить, потому что он используется",
        )
