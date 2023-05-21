from django.test import TestCase
from django.urls import reverse
from posts.models import User, Post
from posts.forms import PostForm
from ..helpers import LogInTest

class FeedViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.url = reverse('feed')
    
    def test_feed_url(self):
        self.assertEqual(self.url, '/feed/')
    
    def test_get_feed(self):
        self.client.login(username=self.user.username, password="Password123") # self.client represents a HTTP client to make HTTP requests (GET, POST etc. with data in body if needed)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)

    def test_get_feed_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + f'?next={self.url}' # Query parameter 'next' holds URL to redirect to after log in
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)