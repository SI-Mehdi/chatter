from django.test import TestCase
from django.urls import reverse
from posts.models import User, Post


class FollowToggleViewTestCase(TestCase):

    fixtures = [
            'posts/tests/fixtures/test_user.json',
            'posts/tests/fixtures/other_users.json'
        ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.to_follow = User.objects.get(username='@janedoe')
        self.url = reverse('follow_toggle', kwargs={'username': self.to_follow.username})


    def test_follow_toggle_url(self):
        self.assertEqual(self.url,'/follow_toggle/@janedoe')
    
    def test_get_follow_toggle_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in') + f'?next={self.url}' # Query parameter 'next' holds URL to redirect to after log in
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_get_follow_toggle_valid_username(self):
        self.client.login(username=self.user.username, password='Password123')

        user_followers_before = self.user.follower_count()
        to_follow_followers_before = self.to_follow.follower_count()

        response = self.client.get(self.url, follow=True)

        user_followers_after = self.user.follower_count()
        to_follow_followers_after = self.to_follow.follower_count()

        self.assertEqual(user_followers_before, user_followers_after)
        self.assertEqual(to_follow_followers_before + 1, to_follow_followers_after)

        redirect_url = reverse('profile', kwargs={'username': self.to_follow.username})

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200) # Assert that the GET request response redirected to the correct profile URL
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_get_follow_toggle_invalid_username(self):
        self.client.login(username=self.user.username, password='Password123')

        bad_url = reverse('follow_toggle', kwargs={'username': "@wrongone"}) # The kwargs dictionary maps parameter names (defined in the URL pattern) to their corresponding values. 
        response = self.client.get(bad_url, follow=True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')