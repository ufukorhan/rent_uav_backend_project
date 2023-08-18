from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    A custom user manager for the User model.

    This manager provides methods for creating regular users and superusers.
    """

    def create_user(self, email: str, password: str, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: The newly created user.
        """
        if not email:
            raise ValueError("Email is required")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.

        Args:
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            **extra_fields: Additional fields to be saved in the user model.

        Returns:
            User: The newly created superuser.
        """
        if not email:
            raise ValueError("Email is required")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
