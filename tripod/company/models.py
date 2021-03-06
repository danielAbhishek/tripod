from django.db import models
from django.contrib.auth import get_user_model

# from company.managers import (PackageManager, ProductManager,
                              # PackageProductManager)


class Event(models.Model):
    """
    Event database object holds the information of event or programe to
    which business user cases will be handled saperatly
    """
    event_name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='eventCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='eventChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.event_name


class Product(models.Model):
    """
    This class only holds the information of the products that is relevent
    for the business packages that sellable to clients or customers
    """
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
    display = models.BooleanField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='productCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='productChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    # objects = ProductManager()

    def __str__(self):
        return self.product_name

    def total_price(self, units):
        return self.unit_price * units

    def calculate_price(self, units):
        price = self.total_price(units)
        return price

    def discounted_price(self, units, discount_percentage):
        price = self.total_price(units)
        discount = price * discount_percentage
        return price - discount

    class Meta:
        ordering = ('product_name', )


class Package(models.Model):
    """
    Package database object
        This has the information of the packages, the customized for each event
        and added with custome products, that eventually will be used to
        attract customers or clients
    """
    package_name = models.CharField(max_length=150)
    description = models.TextField()
    event = models.ForeignKey(Event,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    is_active = models.BooleanField(default=True)
    price = models.FloatField(null=True, blank=True)
    products = models.ManyToManyField(Product, through='PackageLinkProduct')
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='packageCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='packageChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    # objects = PackageManager()

    def __str__(self):
        return self.package_name


class PackageLinkProduct(models.Model):
    """
        An associate table for many-to-many relation
        between package and products
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units = models.FloatField()
    price = models.FloatField()
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='plpCreated',
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    changed_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.SET_NULL,
                                   related_name='plpChanged',
                                   null=True,
                                   blank=True)
    changed_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # objects = PackageProductManager()

    def __str__(self):
        return f"{self.product.product_name} - {self.package.package_name}"

    def calculate_price(self):
        return self.product.calculate_price(self.units)

    def calculate_discounted_price(self, discount_percentage):
        return self.product.discounted_price(self.units, discount_percentage)


class Equipment(models.Model):
    """
    Equipments in the company
    """
    TYPES = [('cu', 'common use'), ('iu', 'individual use')]
    AVAILABILITY = [
        ('na', 'not available'),
        ('av', 'available'),
        ('um', 'under maintanence'),
        ('ml', 'malfunction'),
    ]
    equipment_name = models.CharField(max_length=200)
    e_type = models.CharField(max_length=2, choices=TYPES)
    availability = models.CharField(max_length=2, choices=AVAILABILITY)
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.equipment_name

    def get_e_type(self):
        for x in self.TYPES:
            if x[0] == self.e_type:
                return x[1]

    def get_availability(self):
        for x in self.AVAILABILITY:
            if x[0] == self.availability:
                return x[1]


class EquipmentMaintanence(models.Model):
    """
    Maintanence data for the equipments
    """
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintanence_date = models.DateField()
    next_available_date = models.DateField(null=True, blank=True)
    maintanence_cost = models.FloatField(null=True, blank=True)
    done = models.BooleanField()
    maintanence_reason = models.TextField()

    def __str__(self):
        return self.equipment.equipment_name
