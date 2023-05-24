from django.test import TestCase
from django.urls import reverse
from posts.models import User, Post
from ..helpers import LogInTest

class SearchViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json',
                'posts/tests/fixtures/test_post.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('search') + '?query=e'

    
    def test_search_url(self):
        self.assertEqual(self.url, "/search/?query=e")
    
    def test_search_valid_query(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        users = response.context['users']
        posts = response.context['posts']
        query = response.context['query']
        self.assertEqual(1, len(users))
        self.assertEqual(1, len(posts))
        self.assertEqual("e", query)
    
    def test_search_invalid_query(self):
        self.client.login(username=self.user.username, password="Password123")
        bad_query = reverse('search') + '?query=x'
        response = self.client.get(bad_query)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')
        users = response.context['users']
        posts = response.context['posts']
        query = response.context['query']
        self.assertEqual(0, len(users))
        self.assertEqual(0, len(posts))
        self.assertEqual("x", query)
    
    def test_get_search_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + f'?next={self.url}'
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)