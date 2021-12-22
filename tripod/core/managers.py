from django.contrib.auth.base_user import BaseUserManager
from django.db import models
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

        if extra_fields.get('is_staff'):
            raise ValueError(_('client cannot have is_staff=True'))
        if extra_fields.get('is_superuser'):
            raise ValueError(_('client cannot have is_superuser=True'))
        return self.create_user(email, password, **extra_fields)


class PackageManager(models.Manager):
    """
    Custom class to manage the package and products
    """
    def create_new_package(self, name, description, event):
        package = self.create(package_name=name,
                              description=description,
                              event=event,
                              is_active=True)
        return package


class ProductManager(models.Manager):
    def create_display_product(self, name, price, measure_type, product_type,
                               description):
        product = self.create(product_name=name,
                              unit_price=price,
                              unit_measure_type=measure_type,
                              product_type=product_type,
                              description=description,
                              display=True,
                              is_active=True)
        return product


class PackageProductManager(models.Manager):
    def add_products_to_package(self, package, products):
        """
        products should be a list with below mentioned information
        p = [
            (product, 5.0 <units>),
            (product2, 3.0 <units>),
        ]
        """
        if type(products) is not list:
            raise TypeError('products should be list')

        result = []

        for product in products:
            """
            looping thru product list and validating inputs before 
            processing to create the model instance
            """
            if isinstance(product[1], str):
                raise ValueError('Incorrect unit is passed')

            ppm = self.create(package=package,
                              product=product[0],
                              units=product[1],
                              price=product[0].calculate_price(
                                  product[1], product[2]))

            result.append(ppm)
        return result
