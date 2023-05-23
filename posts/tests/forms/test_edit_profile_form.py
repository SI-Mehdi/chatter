from django.test import TestCase
from django import forms
from django.contrib import messages
from posts.forms import EditProfileForm
from django.urls import reverse
from posts.models import User
from ..helpers import LogInTest

class ProfileFormTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

        self.form_input = {
            'first_name': 'Adam',
            'last_name': 'Smith',
            'email': 'changedemail@new.co.uk',
            'bio': 'Brand new bio for testing'
        }

        self.url = reverse('edit_profile')
    
    def test_valid_form(self):
        form = EditProfileForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_fields(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('bio', form.fields)
        bio_field = form.fields['bio']
        self.assertTrue(isinstance(bio_field.widget, forms.Textarea))
    
    def test_details_are_changed(self):
        self.client.login(username=self.user.username, password="Password123", follow=True)

        before_first_name = self.user.first_name
        before_last_name = self.user.last_name
        before_email = self.user.email
        before_bio = self.user.bio

        response = self.client.post(self.url, self.form_input)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

        self.user.refresh_from_db()  # Refresh user object from the database

        after_first_name = self.user.first_name
        after_last_name = self.user.last_name
        after_email = self.user.email
        after_bio = self.user.bio

        self.assertNotEqual(self.user.first_name, before_first_name)
        self.assertNotEqual(self.user.last_name, before_last_name)
        self.assertNotEqual(self.user.email, before_email)
        self.assertNotEqual(self.user.bio, before_bio)

        self.assertEqual(self.user.first_name, after_first_name)
        self.assertEqual(self.user.last_name, after_last_name)
        self.assertEqual(self.user.email, after_email)
        self.assertEqual(self.user.bio, after_bio)

        self.assertEqual(self.user.first_name, "Adam")
        self.assertEqual(self.user.last_name, "Smith")
        self.assertEqual(self.user.email, "changedemail@new.co.uk")
        self.assertEqual(self.user.bio, "Brand new bio for testing")