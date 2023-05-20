from django.test import TestCase
from django.urls import reverse
from posts.forms import LogInForm
from posts.models import User
from ..helpers import LogInTest

class LogOutViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.url = reverse('log_out')

        self.user = User.objects.get(username="@johndoe")

    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')
    
    def test_get_log_out(self):
        self.client.login(username='@johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())