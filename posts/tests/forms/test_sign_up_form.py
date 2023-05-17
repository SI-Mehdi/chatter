from django.test import TestCase
from posts.forms import SignUpForm
from posts.models import User

class SignUpFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'first_name': "John",
            'last_name': "Doe",
            'username': '@johndoe',
            'email': 'johndoe@test.com',
            'bio': 'Test',
            'password': "Password123",
            'confirm_password': "Password123"
        }

    def test_valid_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_correct_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('bio', form.fields)
        self.assertIn('password', form.fields)
        self.assertIn('confirm_password', form.fields)
    
    def test_username_validation(self):
        self.form_input['username'] = 'incorrectformat'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_password_validation(self):
        self.form_input['password'] = 'wrong'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_save_user_correctly(self):
        before_count = User.objects.count()
        form = SignUpForm(data=self.form_input)
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(username="@johndoe")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, 'johndoe@test.com')
        self.assertEqual(user.bio, 'Test')