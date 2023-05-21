from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import User, Post
from posts.forms import PostForm
from ..helpers import LogInTest

class NewPostViewTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('new_post')
        
        # Open and read the image file
        # Using 'with' statement to ensure that the open function closes the file after reading
        with open('posts/tests/images/test.jpg', 'rb') as file:
            # Create a SimpleUploadedFile object with the file data
            image_data = file.read()
            self.form_data = {
                'title': 'Test Post',
                'image': SimpleUploadedFile('test.jpg', image_data, content_type='image/jpeg'),
                'body': 'Test post body',
            }
    
    def test_new_post_authenticated_user(self):
        self.assertEqual(Post.objects.count(), 0)
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)  # Redirect to 'feed' page
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertIsNotNone(post.image)
        self.assertEqual(post.body, 'Test post body')
        self.assertEqual(post.author, self.user)

    def test_new_post_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(self.url, data=self.form_data)
        
        self.assertEqual(response.status_code, 302)  # Redirect to 'log_in' page
        self.assertEqual(Post.objects.count(), 0)  # No post created

    def test_new_post_invalid_form(self):
        self.client.login(username=self.user.username, password="Password123")
        form_data = {
            'title': '',  # Invalid, required field
        }
        response = self.client.post(self.url, data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)  # Render the 'feed' template with form errors
        self.assertEqual(Post.objects.count(), 0)  # No post created
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTrue(response.context['form'].errors)
        