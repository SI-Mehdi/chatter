from django.test import TestCase
from django.core.exceptions import ValidationError
from posts.models import User,Post

class PostModelTestCase(TestCase):

    fixtures = ['posts/tests/fixtures/test_user.json',
                'posts/tests/fixtures/other_users.json'
                ]

    def setUp(self):
        self.author = User.objects.get(username='@johndoe')
        self.post = Post.objects.create(
            author=self.author,
            title='Test Post',
            image='posts/tests/images/test.jpg',
            body='This is a test post body.'
        )

    def test_valid_post(self):
        self._assert_post_is_valid()

    def test_blank_title_not_allowed(self):
        self.post.title = ''
        self._assert_post_is_invalid()

    def test_blank_body_allowed(self):
        self.post.body = ''
        self._assert_post_is_valid()

    def test_image_blank_or_null_allowed(self):
        self.post.image = None
        self._assert_post_is_valid()

    def _assert_post_is_valid(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test post should be valid")

    def _assert_post_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.post.full_clean()
