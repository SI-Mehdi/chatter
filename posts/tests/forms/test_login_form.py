from django.test import TestCase
from django import forms
from django.contrib import messages
from posts.forms import LogInForm
from django.urls import reverse
from posts.models import User
from ..helpers import LogInTest

class LogInFormTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.form_input = {
            'username': '@johndoe',
            'password': 'Password123'
        }
        self.url = reverse('log_in')
    
    def test_form_fields_correct(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))
    
    def test_valid_input(self):
        form = LogInForm(self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_username(self):
        self.form_input['username'] = ''
        form = LogInForm(self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_password(self):
        self.form_input['password'] = ''
        form = LogInForm(self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_unsuccessful_login(self):
        self.form_input['username'] = "wrong"
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
    
    def test_successful_login(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        response_url = reverse('feed')
        # Checking the response that is created from the POST redirects eventually to response_url
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
    