from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersCRUDAuthTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='alice', password='password123',
            first_name='Alice', last_name='A', email='alice@example.com'
        )
        self.user2 = User.objects.create_user(
            username='bob', password='password123',
            first_name='Bob', last_name='B', email='bob@example.com'
        )

    def test_users_list_accessible_anonymously(self):
        resp = self.client.get(reverse('users:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'alice')
        self.assertContains(resp, 'bob')

    def test_register_redirects_to_login(self):
        resp = self.client.post(reverse('users:create'), {
            'username': 'charlie',
            'first_name': 'Charlie',
            'last_name': 'C',
            'email': 'charlie@example.com',
            'password1': 'StrongPassw0rd!',
            'password2': 'StrongPassw0rd!',
        })
        self.assertRedirects(resp, reverse('login'))
        self.assertTrue(User.objects.filter(username='charlie').exists())

    def test_login_redirects_to_home(self):
        resp = self.client.post(reverse('login'), {
            'username': 'alice',
            'password': 'password123'
        })
        self.assertRedirects(resp, reverse('home'))

    def test_update_self_success(self):
        self.client.login(username='alice', password='password123')
        url = reverse('users:update', args=[self.user1.pk])
        resp = self.client.post(url, {
            'username': 'alice',
            'first_name': 'AliceNew',
            'last_name': 'A',
            'email': 'alice_new@example.com',
        })
        self.assertRedirects(resp, reverse('users:list'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'AliceNew')
        self.assertEqual(self.user1.email, 'alice_new@example.com')

    def test_update_other_denied(self):
        self.client.login(username='alice', password='password123')
        url = reverse('users:update', args=[self.user2.pk])
        resp = self.client.post(url, {
            'username': 'bob',
            'first_name': 'Hacked',
            'last_name': 'B',
            'email': 'hack@example.com',
        })
        self.assertRedirects(resp, reverse('users:list'))
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, 'Bob')

    def test_delete_self(self):
        self.client.login(username='bob', password='password123')
        url = reverse('users:delete', args=[self.user2.pk])
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('users:list'))
        self.assertFalse(User.objects.filter(username='bob').exists())

    def test_delete_other_denied(self):
        self.client.login(username='alice', password='password123')
        url = reverse('users:delete', args=[self.user2.pk])
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('users:list'))
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_logout_post_redirects_to_home(self):
        self.client.login(username='alice', password='password123')
        resp = self.client.post(reverse('logout'))
        self.assertRedirects(resp, reverse('home'))
