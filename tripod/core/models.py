from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from core.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NA', 'Not specified'),
        ('O', 'Others'),
    ]

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER,
        default='NA',
        blank=True,
        null=True,
    )
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    contact_number_2 = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    province = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    force_password_change = models.BooleanField(default=False,
                                                blank=True,
                                                null=True)
    password_change_code = models.CharField(max_length=20,
                                            null=True,
                                            blank=True)
    # created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # changed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # changed_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Company(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField()
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name
