"""
This module contains unit tests for the Django application.

Unit tests are used to test individual units of code in the application, such as models, views, and forms. The tests in this module are based on the Django TestCase class and provide additional functionality for testing the database, sending HTTP requests, and testing forms.

Classes:
* TestCase: The base test case class used for testing Django applications.

Functions:
* setUp: A function that is called before each test method is run.
* tearDown: A function that is called after each test method is run.
* test_*: Functions that define individual test cases.

To define a unit test, create a function that starts with the prefix test_ and define one or more assertions that check the output of the code being tested. The assertions are typically based on the expected output of the code, and should fail if the output does not match the expected value.

Example usage:
# tests.py
from django.test import TestCase
from .models import Book

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Book', author='Test Author')

    def test_book_creation(self):
        self.assertTrue(isinstance(self.book, Book))
        self.assertEqual(self.book.__str__(), 'Test Book')

    def test_book_deletion(self):
        book_count = Book.objects.count()
        self.book.delete()
        self.assertEqual(Book.objects.count(), book_count - 1)

# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# output
Ran 2 tests in 0.001s

OK
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import (
    SignUpForm,
    ChangePassword,
    UserEditForm,
    ProfileEditForm,
    ReSendActivationLink,
)


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user object for testing
        user = get_user_model().objects.create_user(
            username="TestUser", password="testpassword"
        )
        # Create a user profile object for testing
        cls.test_profile = UserProfile.objects.create(
            user=user,
            email_verified=True,
            user_avatar="avatars/test.png",
            user_birthday_date="2000-01-01",
            user_description="A test user profile",
        )

    def test_user_profile_str(self):
        """
        Tests that the __str__() method of a UserProfile object
        returns the expected string.
        """
        expected = f"UserProfile of {self.test_profile.user}"
        self.assertEqual(str(self.test_profile), expected)

    def test_user_has_verified_email(self):
        """
        Tests that the email_verified field is set to True
        for a user profile with a verified email address.
        """
        self.assertTrue(self.test_profile.email_verified)

    def test_user_avatar_path(self):
        """
        Tests that the avatar image field has the correct upload path.
        """
        expected_path = "user_avatars/2022/05/01/test.png"
        self.assertEqual(
            self.test_profile.avatar.path.split("/")[-4:], expected_path.split("/")
        )

    def test_user_birthday_date(self):
        """
        Tests that the birthday date field has the correct value.
        """
        expected_date = "2000-01-01"
        self.assertEqual(str(self.test_profile.birthday), expected_date)

    def test_user_description(self):
        """
        Tests that the description field has the correct value.
        """
        expected_description = "A test user profile"
        self.assertEqual(self.test_profile.description, expected_description)


class SignUpFormTests(TestCase):
    def test_valid_form(self):
        """
        Test whether a valid form is being validated properly.
        """
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password1": "test_password123",
            "password2": "test_password123",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """
        Test whether an invalid email address raises a validation error.
        """
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalidemailaddress",
            "password1": "test_password123",
            "password2": "test_password123",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Enter a valid email address."])

    def test_duplicate_email(self):
        """
        Test whether a duplicate email address raises a validation error.
        """
        # create a user with the same email address
        get_user_model().objects.create_user(
            username="testuser", email="johndoe@example.com"
        )
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password1": "test_password123",
            "password2": "test_password123",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Email already in use!"])


class ChangePasswordFormTests(TestCase):
    def test_valid_form(self):
        """
        Test whether a valid form is being validated properly.
        """
        form_data = {
            "old_password": "test_old_password123",
            "new_passowrd1": "test_new_password123",
            "new_password2": "test_new_password123",
        }
        form = ChangePassword(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_field(self):
        """
        Test whether a missing field raises a validation error.
        """
        form_data = {
            "old_password": "",
            "new_passowrd1": "",
            "new_password2": "",
        }
        form = ChangePassword(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["old_password"], ["This field is required."])
        self.assertEqual(form.errors["new_passowrd1"], ["This field is required."])
        self.assertEqual(form.errors["new_password2"], ["This field is required."])

    def test_mismatched_passwords(self):
        """
        Test whether a mismatched password raises a validation error.
        """
        form_data = {
            "old_password": "test_old_password123",
            "new_passowrd1": "test_new_password123",
            "new_password2": "mismatched_password",
        }
        form = ChangePassword(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["new_password2"], ["Passwords do not match."])


class UserEditFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
        )

    def test_valid_form(self):
        """
        Test whether a valid form is being validated properly.
        """
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
        }
        form = UserEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_missing_field(self):
        """
        Test whether a missing field raises a validation error.
        """
        form_data = {"first_name": "", "last_name": "User", "email": "test@example.com"}
        form = UserEditForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["first_name"], ["This field is required."])

    def test_invalid_email(self):
        """
        Test whether an invalid email address raises a validation error.
        """
        form_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid-email-address",
        }
        form = UserEditForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Enter a valid email address."])


class ProfileEditFormTests(TestCase):
    def setUp(self) -> None:
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            avatar="default-avatar.jpg",
            birthday="1990-01-01",
            description="Test User",
        )

    def test_valid_form(self):
        """
        Test whether a valid form is being validated properly.
        """
        form_data = {
            "avatar": "test-avatar.jpg",
            "birthday": "1991-01-01",
            "description": "Updated test user",
        }
        form = ProfileEditForm(data=form_data, instance=self.user_profile)
        self.assertTrue(form.is_valid())

    def test_missing_field(self):
        """
        Test whether a missing field raises a validation error.
        """
        form_data = {"avatar": "", "birthday": "1991-01-01", "description": "Test User"}
        form = ProfileEditForm(data=form_data, instance=self.user_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["avatar"], ["This field is required."])

    def test_invalid_date(self):
        """
        Test whether an invalid date format raises a validation error.
        """
        form_data = {
            "avatar": "test-avatar.jpg",
            "birthday": "invalid-date-format",
            "description": "Test User",
        }
        form = ProfileEditForm(data=form_data, instance=self.user_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["birthday"], ["Enter a valid date."])


class ReSendActivationLinkFormTests(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_valid_form(self):
        """
        Test whether a valid form is being validated properly.
        """
        form_data = {
            "email": "test@example.com",
        }
        form = ReSendActivationLink(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_email_field(self):
        """
        Test whether an empty email field raises a validation error.
        """
        form_data = {"email": ""}
        form = ReSendActivationLink(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required."])

    def test_invalid_email_address(self):
        """
        Test whether an invalid email address raises a validation error.
        """
        form_data = {"email": "invalid-email-address"}
        form = ReSendActivationLink(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Enter a valid email address."])

    def test_unregistered_email_address(self):
        """
        Test whether an unregistered email address raises a validation error.
        """
        form_data = {"email": "test2@example.com"}
        form = ReSendActivationLink(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            ["This email address does not correspond to an existing user account."],
        )
