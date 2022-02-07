from django.db import models


class PackageManager(models.Manager):
    pass
    """
    Custom class to manage the package and products
    """
    # def create_new_package(self, name, description, event):
    #     package = self.create(package_name=name,
    #                           description=description,
    #                           event=event,
    #                           is_active=True)
    #     return package


class ProductManager(models.Manager):
    pass
    # def create_display_product(self, name, price, measure_type, product_type,
    #                            description):
    #     product = self.create(product_name=name,
    #                           unit_price=price,
    #                           unit_measure_type=measure_type,
    #                           product_type=product_type,
    #                           description=description,
    #                           display=True,
    #                           is_active=True)
    #     return product


class PackageProductManager(models.Manager):
    pass
    # def create_link(self, package, product, units, price):
    #     link = self.create(
    #         package=package,
    #         product=product,
    #         units=units,
    #         price=price)
    #     return link
    #
    # def add_products_to_package(self, package, products):
    #     """
    #     products should be a list with below mentioned information
    #     p = [
    #         (product, 5.0 <units>),
    #         (product2, 3.0 <units>),
    #     ]
    #     """
    #     if type(products) is not list:
    #         raise TypeError('products should be list')
    #
    #     result = []
    #
    #     for product in products:
    #         """
    #         looping thru product list and validating inputs before
    #         processing to create the model instance
    #         """
    #         if isinstance(product[1], str):
    #             raise ValueError('Incorrect unit is passed')
    #
    #         ppm = self.create(package=package,
    #                           product=product[0],
    #                           units=product[1],
    #                           price=product[0].calculate_price(
    #                               product[1], product[2]))
    #
    #         result.append(ppm)
    #     return result
