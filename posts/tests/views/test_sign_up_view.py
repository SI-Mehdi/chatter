from django.test import TestCase
from django.urls import reverse
from posts.models import User
from posts.forms import SignUpForm
from ..helpers import LogInTest

class SignUpViewTestCase(TestCase, LogInTest):
    def setUp(self):
        self.url = reverse("sign_up")

        self.form_input = {
            'first_name': "John",
            'last_name': "Doe",
            'username': '@johndoe',
            'email': 'johndoe@test.com',
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
        user = User.objects.get(username='@johndoe')
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, 'johndoe@test.com')
        self.assertEqual(user.bio, 'Test')
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        self.assertTrue(self._is_logged_in())
        
