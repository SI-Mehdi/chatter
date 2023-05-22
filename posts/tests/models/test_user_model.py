from django.test import TestCase
from django.core.exceptions import ValidationError
from posts.models import User

# Create your tests here.

class UserModelTestCase(TestCase):

    fixtures = ['posts/tests/fixtures/test_user.json',
                'posts/tests/fixtures/other_users.json'
                ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.user_two = User.objects.get(username="@janedoe")

    def test_valid_user(self):
        self._assert_user_is_valid()
    
    def test_must_have_username(self):
        self.user.username = ''
        self._assert_user_is_invalid()
    
    def test_username_can_be_50_characters_long(self):
        self.user.username = '@' + 'x' * 49
        self._assert_user_is_valid()

    def test_username_cannot_be_over_50_characters_long(self):
        self.user.username = '@' + 'x' * 50
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@johndoe'
        self._assert_user_is_invalid()


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()

    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_500_characters(self):
        self.user.bio = 'x' * 500
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_500_characters(self):
        self.user.bio = 'x' * 501
        self._assert_user_is_invalid()

    def test_toggle_follow(self):
        john = User.objects.get(username='@johndoe')
        jane = User.objects.get(username='@janedoe')

        self.assertFalse(john.is_following(jane))
        self.assertFalse(jane.is_following(john))

        john.toggle_follow(jane)

        self.assertTrue(john.is_following(jane))
        self.assertFalse(jane.is_following(john))

        john.toggle_follow(jane)

        self.assertFalse(john.is_following(jane))
        self.assertFalse(jane.is_following(john))


    def test_follow_counters(self):
        john = User.objects.get(username='@johndoe')
        jane = User.objects.get(username='@janedoe')
        jim = User.objects.get(username='@jimdoe')

        self.assertEqual(john.follower_count(), 0)
        self.assertEqual(john.following_count(), 0)

        self.assertEqual(jane.follower_count(), 0)
        self.assertEqual(jane.following_count(), 0)

        self.assertEqual(jim.follower_count(), 0)
        self.assertEqual(jim.following_count(), 0)

        john.toggle_follow(jane)
        jane.toggle_follow(jim)

        self.assertEqual(john.follower_count(), 0)
        self.assertEqual(john.following_count(), 1)

        self.assertEqual(jane.follower_count(), 1)
        self.assertEqual(jane.following_count(), 1)

        self.assertEqual(jim.follower_count(), 1)
        self.assertEqual(jim.following_count(), 0)

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
