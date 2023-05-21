from django.test import TestCase
from django.urls import reverse
from posts.models import User
from posts.forms import SignUpForm
from ..helpers import LogInTest

class SignUpViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json'] # Fixtures create objects from model data given in JSON

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

        self.url = reverse("sign_up")

        self.form_input = {
            'first_name': "Jane",
            'last_name': "Doe",
            'username': '@janedoe',
            'email': 'janedoe@test.com',
            'bio': 'Test',
            'password': "Password123",
            'confirm_password': "Password123"
        }

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_bad_sign_up(self):
        self.form_input['username'] = 'wrongformat'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
    
    def test_good_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, 'janedoe@test.com')
        self.assertEqual(user.bio, 'Test')
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        self.assertTrue(self._is_logged_in())
    
    def test_get_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True) # Follow means follow any redirects, want to be redirected to feed
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
    
    def test_post_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse('feed')
        after = User.objects.count()
        self.assertEqual(before, after)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        
