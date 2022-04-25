from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.forms.models import modelformset_factory

from company.models import (Event, Package, PackageLinkProduct, Product)
from company.forms import (EventForm, ProductForm, PackageForm,
                           PackageLinkProductAddForm, EquipmentForm,
                           EquipmentMaintanenceForm)
from company.tests import fixtures


class EventFormTests(TestCase):

    def setUp(self):
        # creating user
        self.user = get_user_model().objects.create_user(
            'test@gmail.com', 'abcd@1234')
        # creating second user
        self.update_user = get_user_model().objects.create_user(
            'second@gmail.com', 'test@1234')
        # setting fixtures for event creation and updates
        self.add_data = fixtures.events['wedding']
        self.update_data = fixtures.events['birthday']

    def add_creating_event(self):
        """adding a new event via EventForm"""
        form = EventForm(data=self.add_data,
                         userObj=self.user,
                         operation='creating')
        event = form.save()
        return event

    def add_updating_event(self):
        """Changing the content of the already added event obj"""
        event = self.add_creating_event()
        form = EventForm(data=self.update_data,
                         userObj=self.update_user,
                         instance=event,
                         operation='updating')
        obj = form.save()
        return obj

    def test_form_is_valid(self):
        """testing form is valid"""
        form = EventForm(data={
            'event_name': 'Wedding',
            'description': 'wedding event'
        },
                         userObj=self.user,
                         operation='creating')
        self.assertTrue(form.is_valid())

    def test_form_saved_with_values(self):
        """
        testing that passed values are updated correctly
        """
        event = self.add_creating_event()
        self.assertEqual(event.event_name, self.add_data['event_name'])

    def test_form_created_by_added(self):
        """testing that created_by is equal with the user object"""
        event = self.add_creating_event()
        self.assertEqual(event.created_by, self.user)

    def test_form_changed_at_added(self):
        """checking that changed_at timestamp is correctly added"""
        event = self.add_updating_event()
        self.assertEqual(event.created_at.strftime("%Y-%m-%d %H:%M"),
                         timezone.now().strftime("%Y-%m-%d %H:%M"))

    def test_form_changed_by_added(self):
        """
        checking that changed by captured correctly, and created_by
        did not change
        """
        event = self.add_updating_event()
        self.assertEqual(event.changed_by, self.update_user)
        self.assertEqual(event.created_by, self.user)

    def test_updates_added_to_db(self):
        """
        checking if the updates correctly added to database
        """
        event = self.add_updating_event()
        obj = Event.objects.get(id=event.id)
        self.assertEqual(obj.event_name, self.update_data['event_name'])
        self.assertEqual(obj.description, self.update_data['description'])


class ProductFormTest(TestCase):

    def setUp(self):
        # creating user
        self.user = get_user_model().objects.create_user(
            'test@gmail.com', 'abcd@1234')
        # creating another user
        self.update_user = get_user_model().objects.create_user(
            'second@gmail.com', 'test@1234')
        # setting the fixtures for product creation and updates
        self.add_data = fixtures.products['photo frame']
        self.update_data = fixtures.products['short video']

    def add_creating_product(self):
        """adding a new product via ProductForm"""
        form = ProductForm(data=self.add_data,
                           userObj=self.user,
                           operation='creating')
        product = form.save()
        return product

    def add_updating_product(self):
        """Changing the content of the already added product obj"""
        product = self.add_creating_product()
        form = ProductForm(data=self.update_data,
                           userObj=self.update_user,
                           instance=product,
                           operation='updating')
        obj = form.save()
        return obj

    def test_form_is_valid(self):
        """testing form is valid"""
        form = ProductForm(data={
            'product_name': 'photo frame',
            'unit_price': 1000,
            'unit_measure_type': Product.MEASURE_TYPES[0][0],
            'product_type': Product.PRODUCT_TYPES[0][0],
            'description': 'testing 123',
            'display': False,
            'is_active': False
        },
                           userObj=self.user,
                           operation='creating')
        self.assertTrue(form.is_valid())

    def test_form_saved_with_values(self):
        """
        testing that display, and is_active saved with True values
        regardless of the manual input
        """
        product = self.add_creating_product()
        self.assertEqual(product.unit_price, self.add_data['unit_price'])
        self.assertEqual(product.unit_measure_type, 'u')
        self.assertFalse(product.display)
        self.assertTrue(product.is_active)

    def test_form_created_by_added(self):
        """testing that created_by is equal with the user object"""
        product = self.add_creating_product()
        self.assertEqual(product.created_by, self.user)

    def test_form_changed_at_added(self):
        """checking that changed_at timestamp is correctly added"""
        product = self.add_updating_product()
        self.assertEqual(product.created_at.strftime("%Y-%m-%d %H:%M"),
                         timezone.now().strftime("%Y-%m-%d %H:%M"))

    def test_form_changed_by_added(self):
        """
        checking that changed by captured correctly, and created_by
        did not change
        """
        product = self.add_updating_product()
        self.assertEqual(product.changed_by, self.update_user)
        self.assertEqual(product.created_by, self.user)

    def test_updates_added_to_db(self):
        """
        updating the existin product written to database correctly
        """
        product = self.add_updating_product()
        obj = Product.objects.get(id=product.id)
        self.assertEqual(obj.product_name, self.update_data['product_name'])
        self.assertEqual(obj.description, self.update_data['description'])
        self.assertEqual(obj.product_type, self.update_data['product_type'])
        self.assertEqual(obj.unit_price, self.update_data['unit_price'])


class PackageFormTests(TestCase):

    def setUp(self):
        # adding user
        self.user = get_user_model().objects.create_user(
            'test@gmail.com', 'abcd@1234')
        # second user
        self.update_user = get_user_model().objects.create_user(
            'second@gmail.com', 'test@1234')

        # creating event object
        eventForm = EventForm(data=fixtures.events['birthday'],
                              userObj=self.user,
                              operation='creating')
        self.event = eventForm.save()

        # add package data
        self.add_data = fixtures.packages['wedding april']
        self.add_data['event'] = self.event
        # update package data
        self.update_data = fixtures.packages['pre-shoot']
        self.update_data['event'] = self.event

        # setting products and units
        self.products = fixtures.products
        self.units = fixtures.product_units

    def add_creating_package(self):
        """adding a new package via PackageForm"""
        form = PackageForm(data=self.add_data,
                           userObj=self.user,
                           operation='creating')
        package = form.save()
        return package

    def add_updating_package(self):
        """Changing the content of the already added package obj"""
        package = self.add_creating_package()
        form = PackageForm(data=self.update_data,
                           userObj=self.update_user,
                           instance=package,
                           operation='updating')
        obj = form.save()
        return obj

    def add_products_to_package(self, products, units, package):
        """adding products and units to the package"""
        for product in products:
            product_form = ProductForm(data=products[product],
                                       userObj=self.user,
                                       operation='creating')
            product_obj = product_form.save()
            prod_units = units[product]
            form = PackageLinkProductAddForm(data={
                'product': product_obj,
                'units': prod_units
            })
            if form.is_valid():
                obj, package = form.save(package=package,
                                         operation='creating',
                                         userObj=self.user)
        return None

    def test_form_is_valid(self):
        """testing form is valid"""
        form = PackageForm(data={
            'package_name': 'Pre-shoot',
            'description': 'testing description updated',
            'event': self.event,
            'is_active': False,
        },
                           userObj=self.user,
                           operation='creating')
        self.assertTrue(form.is_valid())

    def test_form_saved_with_values(self):
        """
        testing that passed values are updated correctly
        """
        package = self.add_creating_package()
        self.assertEqual(package.package_name, self.add_data['package_name'])
        self.assertEqual(package.price, 0)

    def test_form_created_by_added(self):
        """testing that created_by is equal with the user object"""
        package = self.add_creating_package()
        self.assertEqual(package.created_by, self.user)

    def test_form_changed_at_added(self):
        """checking that changed_at timestamp is correctly added"""
        package = self.add_updating_package()
        self.assertEqual(package.created_at.strftime("%Y-%m-%d %H:%M"),
                         timezone.now().strftime("%Y-%m-%d %H:%M"))

    def test_form_changed_by_added(self):
        """
            checking that changed by captured correctly, and created_by
            did not change
        """
        package = self.add_updating_package()
        self.assertEqual(package.changed_by, self.update_user)
        self.assertEqual(package.created_by, self.user)

    def test_updates_added_to_db(self):
        """
        changing existing package, will be written to db correctly
        """
        package = self.add_updating_package()
        obj = Package.objects.get(id=package.id)
        self.assertEqual(obj.package_name, self.update_data['package_name'])
        self.assertEqual(obj.description, self.update_data['description'])
        self.assertEqual(package.price, 0)

    def test_adding_products_to_package(self):
        """adding products to package and testing the products are there"""
        package = self.add_updating_package()
        self.add_products_to_package(self.products, self.units, package)
        package.save()
        package_obj = Package.objects.get(id=package.id)
        plp = PackageLinkProduct.objects.filter(package=package_obj)
        self.assertEqual(len(plp), 3)

    def test_package_amount_after_products_to_package(self):
        """adding products to package and testing the the total price"""
        package = self.add_updating_package()
        self.add_products_to_package(self.products, self.units, package)
        package.save()
        package_obj = Package.objects.get(id=package.id)
        self.assertEqual(package_obj.price, 43000.00)

    def test_changin_product_in_package_and_testing_amount(self):
        """updating product list in package and checking the total amount after"""
        package = self.add_updating_package()
        self.add_products_to_package(self.products, self.units, package)
        package.save()

        # product
        prod = Product.objects.get(product_name='photo frame')
        package_obj = Package.objects.get(id=package.id)
        plp_instance = PackageLinkProduct.objects.filter(
            package=package_obj)[0]
        form = PackageLinkProductAddForm(instance=plp_instance,
                                         data={
                                             'product': prod,
                                             'units': 1
                                         })
        new_package = None
        if form.is_valid():
            obj, new_package = form.save(package=package,
                                         operation='updating',
                                         userObj=self.user)

        print(form.errors)
        self.assertEqual(new_package.price, 41000.00)


class EquipmentFormTests(TestCase):

    def setUp(self):
        # create user
        self.user = get_user_model().objects.create_user(
            'test@gmail.com', 'abcd@1234')
        # setting fixtures
        self.equip_data = fixtures.equipments
        self.equip_main_data = fixtures.equipment_maintanence

    def create_equipment(self):
        """creating equipments in db"""
        data = self.equip_data["dslr camera"]
        form = EquipmentForm(data=data)
        equip = form.save()
        return equip

    def update_equipment(self):
        """updating equipment in db"""
        data = self.equip_data["wide lens"]
        equip_inst = self.create_equipment()
        form = EquipmentForm(instance=equip_inst, data=data)
        return form.save()

    def test_creating_equipment(self):
        """creating equipment testing"""
        equip = self.create_equipment()

        self.assertEqual(equip.equipment_name, "DSLR camera")

    def test_updating_equipment(self):
        """updating equipment instance testing"""
        equip = self.update_equipment()

        self.assertEqual(equip.equipment_name, "wide lens")

    def test_creating_maintanance_equipment(self):
        """creating a new maintenance task for equipment"""
        equip = self.create_equipment()
        self.equip_main_data['dslr_maintanence']['equipment'] = equip
        form = EquipmentMaintanenceForm(
            data=self.equip_main_data['dslr_maintanence'])
        equip_main = form.save()

        self.assertEqual(equip_main.maintanence_cost, 1000)
        self.assertEqual(equip_main.equipment, equip)
