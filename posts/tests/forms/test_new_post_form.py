from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import User, Post
from posts.forms import PostForm
from ..helpers import LogInTest

class NewPostFormTestCase(TestCase, LogInTest):

    fixtures = ['posts/tests/fixtures/test_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('new_post')
        
        # Open and read the image file
        # Using 'with' statement to ensure that the open function closes the file after reading
        # Can do it because open is a context manager with "__enter__" and "__exit__" methods defined
        with open('posts/tests/images/test.jpg', 'rb') as file:
            # Create a SimpleUploadedFile object with the file data
            image_data = file.read()
            self.form_data = {
                'title': 'Test Post',
                'image': SimpleUploadedFile('test.jpg', image_data, content_type='image/jpeg'),
                'body': 'Test post body',
            }

    def test_valid_form(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, data=self.form_data)

        self.assertEqual(response.status_code, 302)  # Redirect to 'feed' page
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.image.name)
        self.assertEqual(post.body, 'Test post body')

    def test_invalid_form_missing_title(self):
        self.client.login(username=self.user.username, password="Password123")
        form_data = {
            'image': self.form_data['image'],
            'body': self.form_data['body'],
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)  # Render the 'feed' template with form errors
        self.assertEqual(Post.objects.count(), 0)  # No post created
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)
    
    def test_invalid_form_bad_file(self):
        self.client.login(username=self.user.username, password="Password123")
        form_data = {
            'title': 'Test Post',
            'image': SimpleUploadedFile('test.txt', b'Invalid file content', content_type='text/plain'),
            'body': 'Test post body',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)  # Render the 'new_post' template with form errors
        self.assertEqual(Post.objects.count(), 0)  # No post created
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('image', response.context['form'].errors)
