from django.test import TestCase
from django.urls import reverse
from posts.forms import EditProfileForm
from posts.models import User
from ..helpers import LogInTest

class EditProfileViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.url = reverse('edit_profile')

        self.form_input = {
            'first_name': 'Adam',
            'last_name': 'Smith',
            'email': 'changedemail@new.co.uk',
            'bio': 'Brand new bio for testing'
        }

        self.user = User.objects.get(username="@johndoe")

    def test_edit_profile_url(self):
        self.assertEqual(self.url, '/edit_profile/')
    
    def test_get_edit_profile(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
    
    def test_get_edit_profile_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + f'?next={self.url}' # Query parameter 'next' holds URL to redirect to after log in
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)