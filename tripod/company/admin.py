from django.contrib import admin
from company.models import Event, Product, Package, PackageLinkProduct


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event_name', 'description', 'created_by', 'created_at',
        'changed_by', 'changed_at')


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name', 'unit_price', 'created_by', 'created_at',
        'changed_by', 'changed_at')


admin.site.register(Event, EventAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Package)
admin.site.register(PackageLinkProduct)
