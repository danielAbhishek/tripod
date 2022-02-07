from company.models import Event, Product, Package, PackageLinkProduct
from django import forms


def add_basic_html_tags(main_component, field_name):
    data = {
        "placeholder": f"{main_component}-{field_name}",
        "class": "form-control"
    }
    return data


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
    class Meta:
        model = Event
        fields = ['event_name', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.instance:
            obj = Event.objects.get(pk=self.instance.pk)
            self.created_by = obj.created_by
            self.created_at = obj.created_at
            self.id = obj.id
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                add_basic_html_tags("Event", str(field))
            )
        self.fields['description'].widget.attrs.update({'rows': '2'})

    def save(self, *args, **kwargs):
        if self.operation == 'creating':
            self.instance.created_by = self.user
        else:
            self.instance.created_by = self.created_by
            self.instance.created_at = self.created_at
            self.instance.id = self.id
            self.instance.changed_by = self.user
        eventObj = super(EventForm, self).save(*args, **kwargs)
        return eventObj


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_at', 'changed_at', 'created_by', 'changed_by']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        obj = Product.objects.get(pk=self.instance.pk)
        self.created_by = obj.created_by
        self.created_at = obj.created_at
        self.id = obj.id
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                add_basic_html_tags("Product", str(field))
            )
        self.fields['description'].widget.attrs.update({'rows': '2'})

    def save(self, *args, **kwargs):
        self.instance.created_by = self.created_by
        self.instance.created_at = self.created_at
        self.instance.id = self.id
        self.instance.changed_by = self.user
        productObj = super(ProductUpdateForm, self).save(*args, **kwargs)
        return productObj


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 'unit_price',
            'unit_measure_type', 'product_type', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                add_basic_html_tags("Product", str(field))
            )
        self.fields['description'].widget.attrs.update({'rows': '2'})

    def save(self, *args, **kwargs):
        self.instance.created_by = self.user
        self.instance.display = True
        self.is_active = True
        productObj = super(ProductAddForm, self).save(*args, **kwargs)
        return productObj


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['package_name', 'description', 'event']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        self.operation = kwargs.pop('operation')
        super().__init__(*args, **kwargs)
        if self.operation == 'updating':
            self.obj = Package.objects.get(pk=self.instance.pk)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                add_basic_html_tags("Package", str(field))
            )
        self.fields['description'].widget.attrs.update({'rows': '4'})

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
    class Meta:
        model = PackageLinkProduct
        fields = ['product', 'units']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                add_basic_html_tags("Package", str(field))
            )

    def save(self, *args, **kwargs):
        self.package = kwargs.pop('package')
        self.instance.package = self.package
        units = self.instance.units
        unit_price = self.instance.product.unit_price
        self.instance.price = units * unit_price
        obj = super(PackageLinkProductAddForm, self).save(*args, **kwargs)
        self.package = update_package_after_adding_products(self.package)
        return obj, self.package
