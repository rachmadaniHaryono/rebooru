import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# defines utility functions that are available directly
# on an Account object
class AccountManager(BaseUserManager):
    # BaseUserManager provides normalize_email and mak_random_password
    # as well as get_by_natural_key which returns the username

    def create_user(self, username, password):
        """
        Creates and saves an account with a name and password
        """
        if not username:
            # a username is required
            raise ValueError("Users must have a username")
        if not password:
            # a password is required
            raise ValueError("Users must have a password")

        account = self.model(username=username)

        account.set_password(password)
        account.save(using=self._db)

        return account

    def create_superuser(self, username, password):
        account = self.create_user(username, password)

        account.is_staff = True
        account.is_superuser = True
        account.save(using=self._db)

        return account


class Account(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser provides password and last_login
    # PermissionsMixin provides permissions (duh) and user groups

    # username: max 30 chars, letters/numbers/@/./-/_ allowed
    username = models.CharField(max_length=30, unique=True,
                    help_text="Required. 30 characters or fewer. Letters, "
                              "numbers, and @/./-/_ characters",
                    validators=[
                        validators.RegexValidator(
                                re.compile('^[\w.@+-]+$'),
                                "Enter a valid username.",
                                'invalid'
                        )
                    ]
               )

    # email isn't required because why not
    email = models.EmailField("email address", blank=True,
                    help_text="Not required, but available as an option for "
                              "password resets."
            )

    # for when the account was created
    date_joined = models.DateTimeField(auto_now_add=True)

    # for knowing when an account is banned or something
    # but we still wanna have the data around
    is_active = models.BooleanField(default=True)

    # for testing if a user is allowed to log into the admin
    is_staff = models.BooleanField(default=False)

    # profile stuff
    bio = models.TextField(blank=True)
    site = models.URLField(blank=True)

    # use our manager class to add functions to the objects property
    objects = AccountManager()

    # stuff for integrating this user model into stock auth stuff
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['-date_joined']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username
