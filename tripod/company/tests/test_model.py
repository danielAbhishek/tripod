# from django.test import TestCase
#
# from company.models import Event, Package, PackageLinkProduct, Product
#
#
# product_with_tunits = [[
#     'pre-shoot frame', 3000.0, 'u', 'fr', 'photo frame', 2.0, 0.5
# ], ['pre-shoot album', 30000.0, 'u', 'al', 'photo album', 1.0,
#     0], ['pre-shoot', 3000.0, 'h', 'vd', 'pre-shoot video', 1.5, 0.15]]
#
#
# class PackageManagerTests(TestCase):
#     """Testcases for package manager class, creating packages"""
#     def setUp(self):
#         self.event = Event.objects.create(event_name='preshoot_event',
#                                           description='preshoot')
#
#     def test_create_package(self):
#         """testing creating package"""
#         package = Package.objects.create_new_package(
#             name='preshoot', description='preshoot preshoot', event=self.event)
#         self.assertEqual(package.package_name, 'preshoot')
#         self.assertEqual(package.event.event_name, 'preshoot_event')
#         self.assertTrue(package.is_active)
#
#
# class ProductManagerTests(TestCase):
#     """Testcases for product manager class, creating products"""
#     def setUp(self):
#         self.measure_type = Product.UNIT
#         self.product_type = Product.FRAME
#
#     def test_create_product(self):
#         """testing creating products"""
#         product = Product.objects.create_display_product(
#             name='album',
#             price=20.0,
#             measure_type=self.measure_type,
#             product_type=self.product_type,
#             description='example product')
#         self.assertEqual(product.product_name, 'album')
#         self.assertEqual(product.unit_measure_type, 'u')
#         self.assertEqual(product.product_type, 'fr')
#         self.assertTrue(product.display)
#         self.assertTrue(product.is_active)
#
#
# class PackageProductMangerTests(TestCase):
#     """Testcases for adding created products to relevent package"""
#     def setUp(self):
#         # creating an event
#         self.event = Event.objects.create(event_name='preshoot_event',
#                                           description='preshoot')
#         # creating package
#         self.package = Package.objects.create_new_package(
#             name='preshoot', description='preshoot preshoot', event=self.event)
#         # product data variables
#         self.measure_type = Product.UNIT
#         self.product_type = Product.FRAME
#         self.product_name = 'frame'
#         self.product_price = 20.0
#         self.product_des = "example description"
#         self.total_units = 5.0
#         self.products = None
#         # fixtures date
#         self.products_fixtures = product_with_tunits
#
#     @staticmethod
#     def create_display_product_with_tunits(name,
#                                            price,
#                                            mtype,
#                                            ptype,
#                                            des,
#                                            tunits,
#                                            dp=0):
#         """static method to create display product with the total units"""
#         product = (Product.objects.create_display_product(name=name,
#                                                           price=price,
#                                                           measure_type=mtype,
#                                                           product_type=ptype,
#                                                           description=des),
#                    tunits, dp)
#         return product
#
#     def test_add_products_to_package(self):
#         """
#         testing adding products to package, experimenting adding
#         only one product
#         """
#         self.products = self.create_display_product_with_tunits(
#             self.product_name, self.product_price, self.measure_type,
#             self.product_type, self.product_des, self.total_units)
#         ppm = PackageLinkProduct.objects.add_products_to_package(
#             package=self.package, products=[
#                 self.products,
#             ])
#         self.assertEqual(ppm[0].package.package_name, 'preshoot')
#         self.assertEqual(ppm[0].product.product_name, 'frame')
#         self.assertEqual(ppm[0].product.unit_measure_type, 'u')
#         self.assertEqual(ppm[0].product.product_type, 'fr')
#         self.assertEqual(ppm[0].units, 5.0)
#         self.assertEqual(ppm[0].price, 100.0)
#         self.assertEqual(ppm[0].product.unit_price, 20.0)
#
#     def test_raise_typerror_when_product_is_not_list(self):
#         """raise type error if the products argument got other than list"""
#         with self.assertRaises(TypeError):
#             PackageLinkProduct.objects.add_products_to_package(
#                 package=self.package, products=self.products)
#
#     def test_raise_typerror_when_units_got_other_than_numbers(self):
#         """raise type error if unit got any parameter other than numbers"""
#         with self.assertRaises(ValueError):
#             self.products = self.create_display_product_with_tunits(
#                 self.product_name, self.product_price, self.measure_type,
#                 self.product_type, self.product_des, 'five')
#             PackageLinkProduct.objects.add_products_to_package(
#                 self.package, [self.products])
#
#     def test_adding_multiple_products_to_package(self):
#         """adding multiple products to package"""
#         self.products = [
#             self.create_display_product_with_tunits(p[0], p[1], p[2], p[3],
#                                                     p[4], p[5])
#             for p in self.products_fixtures
#         ]
#         ppm = PackageLinkProduct.objects.add_products_to_package(
#             self.package, self.products)
#
#         self.assertEqual(ppm[0].product.product_name, 'pre-shoot frame')
#         self.assertEqual(ppm[1].product.product_name, 'pre-shoot album')
#         self.assertEqual(ppm[2].product.product_type, 'vd')
#         self.assertEqual(ppm[1].price, 30000.0)
#         self.assertEqual(ppm[2].price, 4500.0)
#         self.assertEqual(ppm[0].units, 2.0)
#
#     def test_adding_discounted_price(self):
#         """adding discount to the total price and testing the cases"""
#         self.products = [
#             self.create_display_product_with_tunits(p[0], p[1], p[2], p[3],
#                                                     p[4], p[5], p[6])
#             for p in self.products_fixtures
#         ]
#         ppm = PackageLinkProduct.objects.add_products_to_package(
#             self.package, self.products)
#
#         self.assertEqual(ppm[0].price, 3000.0)
#         self.assertEqual(ppm[1].price, 30000.0)
