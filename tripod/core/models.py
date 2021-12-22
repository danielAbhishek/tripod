from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from core.managers import (CustomUserManager, PackageManager, ProductManager,
                           PackageProductManager)


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.event_name


class Package(models.Model):
    package_name = models.CharField(max_length=150)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    objects = PackageManager()

    def __str__(self):
        return self.package_name


class Product(models.Model):
    # measure types
    UNIT = 'u'
    MINUTE = 'm'
    HOUR = 'h'
    DAY = 'd'
    GIGABYTE = 'gb'

    # product types
    PHOTOGRAPHY = 'ph'
    VIDEOGRAPHY = 'vd'
    FRAME = 'fr'
    ALBUM = 'al'
    OTHER_PRODUCTS = 'op'

    # measure types choices
    MEASURE_TYPES = [(UNIT, 'Unit'), (MINUTE, 'Minute'), (HOUR, 'Hour'),
                     (DAY, 'Day'), (GIGABYTE, 'Gigabytes')]

    # product type choices
    PRODUCT_TYPES = [
        (PHOTOGRAPHY, 'photography'),
        (VIDEOGRAPHY, 'videography'),
        (FRAME, 'frame'),
        (ALBUM, 'album'),
        (OTHER_PRODUCTS, 'other products'),
    ]
    product_name = models.CharField(max_length=200)
    unit_price = models.FloatField()
    unit_measure_type = models.CharField(max_length=2, choices=MEASURE_TYPES)
    product_type = models.CharField(max_length=2, choices=PRODUCT_TYPES)
    description = models.TextField()
    display = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.product_name

    def total_price(self, units):
        return self.unit_price * units

    def calculate_price(self, units, discount_percentage):
        price = self.total_price(units)
        discount = price * discount_percentage
        return price - discount


class PackageLinkProduct(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.FloatField()
    price = models.FloatField()

    objects = PackageProductManager()

    def __str__(self):
        return f"{self.product.product_name} - {self.package.package_name}"

    def calculate_price(self):
        return self.product.calculate_price(self.units)

    def calculate_discounted_price(self, discount_percentage):
        return self.product.discounted_price(self.units, discount_percentage)
