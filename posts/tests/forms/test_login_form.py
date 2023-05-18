from django.test import TestCase
from django import forms
from posts.forms import LogInForm

class LogInFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'username': '@johndoe',
            'password': 'Password123'
        }
    
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