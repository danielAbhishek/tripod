from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the identifier (unique)
    for authentication instead of the username
    """

    def create_user(self, email, password, **extra_fields):
        """
        create and save user with give email and password
        """
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save a superuser with the given email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_client', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('super user must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('super user must have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)

    def create_client(self, email, password, **extra_fields):
        """
        create and save a client account with the given email and password
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_client', True)
        extra_fields.setdefault('force_password_change', True)
        extra_fields.setdefault('is_photographer', False)

        if extra_fields.get('is_staff'):
            raise ValueError(_('client cannot have is_staff=True'))
        if extra_fields.get('is_superuser'):
            raise ValueError(_('client cannot have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)

    def create_staff(self, email, password, username, **extra_fields):
        """
        create and save a staff account with the given email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_client', False)
        extra_fields.setdefault('username', username)
        extra_fields.setdefault('force_password_change', True)
        extra_fields.setdefault('is_photographer', False)

        if extra_fields.get('is_superuser'):
            raise ValueError(_('client cannot have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)
