from django.test import TestCase
from django.urls import reverse
from posts.models import User, Post


class ProfileViewTestCase(TestCase):

    fixtures = [
            'posts/tests/fixtures/test_user.json',
            'posts/tests/fixtures/other_users.json'
        ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('profile', kwargs={'username': self.user.username})


    def test_profile_url(self):
        self.assertEqual(self.url,'/profile/@johndoe')

    def test_get_profile_valid_username(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_get_profile_invalid_username(self):
        self.client.login(username=self.user.username, password='Password123')
        bad_url = reverse('profile', kwargs={'username': "@wrongone"})
        response = self.client.get(bad_url)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    
    def test_get_profile_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + f'?next={self.url}' # Query parameter 'next' holds URL to redirect to after log in
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)