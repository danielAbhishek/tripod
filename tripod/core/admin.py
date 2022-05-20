from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import CustomUserCreationForm, CustomUserChangeFormAdminView
from core.models import CustomUser, Company


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeFormAdminView
    model = CustomUser
    list_display = (
        'email',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_client', 'is_superuser')
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields':
            ('first_name', 'last_name', 'username', 'gender', 'contact_number',
             'contact_number_2', 'address', 'address_2', 'city', 'province',
             'country', 'force_password_change', 'password_change_code')
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': (
            'email',
            'password1',
            'password2',
            'is_staff',
            'is_client',
            'is_active',
        )
    }), )
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)
