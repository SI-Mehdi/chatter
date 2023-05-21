from django.test import TestCase
from django.urls import reverse
from posts.forms import LogInForm
from posts.models import User
from ..helpers import LogInTest

class LogInViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.url = reverse('log_in')

        self.form_input = {
            'username': '@johndoe',
            'password': 'Password123'
        }

        self.user = User.objects.get(username="@johndoe")

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')
    
    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
    
    def test_inactive_login(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
    
    def test_get_login_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True) # Follow means follow any redirects, want to be redirected to feed
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
    
    def test_post_login_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        form_input = {
            'username': '@random',
            'password': 'Password123'
        }
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
