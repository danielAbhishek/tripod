from company.models import Event, Product, Package, PackageLinkProduct
from django import forms


def add_basic_html_tags(main_component, fields, description=False):
    for field in fields:
        fields[str(field)].widget.attrs.update(
            {
                "placeholder": f"{main_component}-str(field)",
                "class": "form-control"
            }
        )
    if description:
        fields['description'].widget.attrs.update({'rows': '2'})


def update_package_after_adding_products(package):
    plp_objs = PackageLinkProduct.objects.filter(package=package)
    if plp_objs.exists():
        total_price = 0
        for obj in plp_objs:
            total_price += obj.units * obj.product.unit_price
        package.price = total_price
    else:
        package.price = 0
    return package


class EventForm(forms.ModelForm):
    """
    Event form that handles the adding new event and updating event info that
    object that available in the database

    --> initialized with (userObj, operation)
        * userObj - user class
        * operation - 'creating' or 'updating'
        * if the operation is updating then created_at and created_by will
            be taken from database
    --> while saving
        * instance id will be populated for update operation
        * data will be automatically populated for below columns
            (created_by, created_at, change_by)
    """
    class Meta:
        model = Event
        fields = ['event_name', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = Event.objects.get(pk=self.instance.pk)
        add_basic_html_tags("Event", self.fields, True)

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.created_by = self.user
        else:
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.id = self.obj.id
            self.instance.changed_by = self.user
        eventObj = super(EventForm, self).save(*args, **kwargs)
        return eventObj


class ProductForm(forms.ModelForm):
    """
    Product form that handles the adding new product and
    updating event info that object that available in the database

    --> initialized with (userObj, operation)
        * userObj - user class
        * operation - 'creating' or 'updating'
        * if the operation is updating then created_at and created_by will
            be taken from database
    --> while saving
        * if adding new record, then display, and is_active will get true
            by default
        * instance id will be populated for update operation
        * data will be automatically populated for below columns
            (created_by, created_at, change_by)
    """
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_at', 'changed_at', 'created_by', 'changed_by']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = Product.objects.get(pk=self.instance.pk)
        add_basic_html_tags("Event", self.fields, True)

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.created_by = self.user
            self.instance.display = True
            self.instance.is_active = True
        else:
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.id = self.obj.id
            self.instance.changed_by = self.user
        productObj = super(ProductForm, self).save(*args, **kwargs)
        return productObj


class PackageForm(forms.ModelForm):
    """
    Package form that handles the adding new product and
    updating event info that object that available in the database

    --> initialized with (userObj, operation)
        * userObj - user class
        * operation - 'creating' or 'updating'
        * if the operation is updating then created_at and created_by will
            be taken from database
    --> while saving
        * if adding new record is_active will get true
            by default
        * instance id will be populated for update operation
        * data will be automatically populated for below columns
            (created_by, created_at, change_by)
        * also package instance price will be recalculated based on products
            that added thru many-to-many through table
    """
    class Meta:
        model = Package
        fields = ['package_name', 'description', 'event']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = Package.objects.get(pk=self.instance.pk)
        add_basic_html_tags("Event", self.fields, True)

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.created_by = self.user
            self.instance.is_active = True
        else:
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.id = self.obj.id
            self.instance.price = self.obj.price
            self.instance.changed_by = self.user

        self.instance = update_package_after_adding_products(self.instance)
        packageObj = super(PackageForm, self).save(*args, **kwargs)
        return packageObj


class PackageLinkProductAddForm(forms.ModelForm):
    """
    PackageLinkProduct form that handles the adding new product and
    updating event info that object that available in the database

    --> while saving with (userObj, operation)
        * userObj - user class
        * operation - 'creating' or 'updating'
        * if the operation is updating then created_at and created_by will
            be taken from database
        * instance id will be populated for update operation
        * data will be automatically populated for below columns
            (created_by, created_at, change_by)
        * also package instance price will be recalculated based on products
            that added thru many-to-many through table
    """
    class Meta:
        model = PackageLinkProduct
        fields = ['product', 'units']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_basic_html_tags("Event", self.fields)

    def save(self, *args, **kwargs):
        self.package = kwargs.pop('package')
        self.operation = kwargs.pop('operation')
        self.user = kwargs.pop('userObj')
        self.instance.package = self.package
        units = self.instance.units
        unit_price = self.instance.product.unit_price
        self.instance.price = units * unit_price
        if self.operation == 'creating':
            self.instance.created_by = self.user
        else:
            self.obj = PackageLinkProduct.objects.get(pk=self.instance.pk)
            self.instance.created_by = self.obj.created_by
            self.instance.created_at = self.obj.created_at
            self.instance.changed_by = self.user
        obj = super(PackageLinkProductAddForm, self).save(*args, **kwargs)
        self.package = update_package_after_adding_products(self.package)
        return obj, self.package
