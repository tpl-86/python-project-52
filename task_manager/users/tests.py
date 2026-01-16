from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersCRUDTests(TestCase):
    fixtures = ['users.json']  # загрузит из users/fixtures/users.json

    def setUp(self):
        self.alice = User.objects.get(pk=1)
        self.bob = User.objects.get(pk=2)

    # C — регистрация
    def test_register_redirects_to_login(self):
        resp = self.client.post(reverse('users:create'), {
            'first_name': 'Charlie',
            'last_name': 'C',
            'username': 'charlie',
            # Пароль подобран под простое правило (>= 3 цифр).
            # Если у вас включены стандартные валидаторы Django (минимум 8 и т.д.),
            # используйте, например, 'Str0ngPass123'.
            'password1': 'a1b2c3',
            'password2': 'a1b2c3',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('login'))
        self.assertTrue(User.objects.filter(username='charlie').exists())

    # U — обновление (своего профиля)
    def test_update_self_success(self):
        self.client.force_login(self.alice)
        url = reverse('users:update', args=[self.alice.pk])
        resp = self.client.post(url, {
            'first_name': 'AliceNew',
            'last_name': 'A',
            'username': 'alice',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('users:list'))
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.first_name, 'AliceNew')

    # U — попытка обновить другого пользователя запрещена
    def test_update_other_denied(self):
        self.client.force_login(self.alice)
        url = reverse('users:update', args=[self.bob.pk])
        resp = self.client.post(url, {
            'first_name': 'Hacked',
            'last_name': 'B',
            'username': 'bob',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('users:list'))
        self.bob.refresh_from_db()
        self.assertEqual(self.bob.first_name, 'Bob')

    # D — удаление самого себя
    def test_delete_self(self):
        self.client.force_login(self.bob)
        url = reverse('users:delete', args=[self.bob.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('users:list'))
        self.assertFalse(User.objects.filter(pk=self.bob.pk).exists())

    # D — удаление другого пользователя запрещено
    def test_delete_other_denied(self):
        self.client.force_login(self.alice)
        url = reverse('users:delete', args=[self.bob.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('users:list'))
        self.assertTrue(User.objects.filter(pk=self.bob.pk).exists())