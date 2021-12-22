from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import CustomUserCreationForm, CustomUserChangeForm
from core.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
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
            'fields': ('is_staff', 'is_active')
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': (
                'first_name',
                'last_name',
                'username',
                'gender',
                'contact_number',
                'contact_number_2',
                'address',
                'address_2',
                'city',
                'province',
                'country',
            )
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': (
            'email',
            'password',
            'password2',
            'is_staff',
            'is_client',
            'is_active',
        )
    }), )
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(CustomUser, CustomUserAdmin)
