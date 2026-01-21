from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsersCRUDTests(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.alice = User.objects.get(pk=1)
        self.bob = User.objects.get(pk=2)

    def test_register_redirects_to_login(self):
        resp = self.client.post(
            reverse("users:create"),
            {
                "first_name": "Charlie",
                "last_name": "C",
                "username": "charlie",
                "password1": "a1b2c3",
                "password2": "a1b2c3",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("login"))
        self.assertTrue(User.objects.filter(username="charlie").exists())

    def test_update_self_success(self):
        self.client.force_login(self.alice)
        url = reverse("users:update", args=[self.alice.pk])
        resp = self.client.post(
            url,
            {
                "first_name": "AliceNew",
                "last_name": "A",
                "username": "alice",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("users:list"))
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.first_name, "AliceNew")

    def test_update_other_denied(self):
        self.client.force_login(self.alice)
        url = reverse("users:update", args=[self.bob.pk])
        resp = self.client.post(
            url,
            {
                "first_name": "Hacked",
                "last_name": "B",
                "username": "bob",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("users:list"))
        self.bob.refresh_from_db()
        self.assertEqual(self.bob.first_name, "Bob")

    def test_delete_self(self):
        self.client.force_login(self.bob)
        url = reverse("users:delete", args=[self.bob.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("users:list"))
        self.assertFalse(User.objects.filter(pk=self.bob.pk).exists())

    def test_delete_other_denied(self):
        self.client.force_login(self.alice)
        url = reverse("users:delete", args=[self.bob.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("users:list"))
        self.assertTrue(User.objects.filter(pk=self.bob.pk).exists())
