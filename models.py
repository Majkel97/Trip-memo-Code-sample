"""
This module contains classes for defining the database schema in Django.

Models are used to define the tables in the database and the relationships between them. The classes in this module are based on the Django Model class and provide additional functionality for customizing fields, adding validation rules, and defining relationships.

Classes:
* Model: The base model class used for defining database tables.
* fields: A module that contains classes for defining model fields.
* query: A module that contains classes for defining database queries.

To use a model in a Django view, import the model class and use it to query the database. The results of the query can be passed to the view's context dictionary and rendered in the template.
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A  model that extends a user profile table in a database.

    Attributes:
    - user: One-to-one relationship with the user model defined by the `get_user_model()` function. This field is the primary key for this table and is required (`blank=False`, `null=False`).
    - email_verified: A boolean field that indicates whether the user has verified their email address. The default value is `False`.
    - user_avatar: An image field that stores the user's avatar image. The images are uploaded to a folder named `users/` followed by the year, month, and day of the upload date. This field is optional (`blank=True`, `null=True`).
    - user_birthday_date: A date field that stores the user's birthday. This field is optional (`blank=True`, `null=True`).
    - user_description: A text field that stores a description of the user. This field is optional (`blank=True`, `null=True`).

    Methods:
    - __str__(self): Returns a string representation of the `UserProfile` object, which includes the username of the associated user.

    Meta options:
    - db_table: This option specifies the name of the database table that this model maps to. In this case, it is set to `"user_profile_table"`.

    Note: The `get_user_model()` function is a convenience function provided by Django that returns the user model that is currently active in the project.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        primary_key=True,
        related_name="profile",
    )
    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to="user_avatars/%Y/%m/%d/", blank=True, null=True
    )
    birthday = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return f"UserProfile of {self.user}"
