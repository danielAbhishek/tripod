import string
import random


def add_basic_html_tags(main_component, fields, description=False):
    for field in fields:
        fields[str(field)].widget.attrs.update({
            "placeholder": f"{main_component}-{str(field)}",
            "class": "form-control"
        })
    if description:
        fields['description'].widget.attrs.update({'rows': '2'})


def staff_check(user):
    return user.is_staff


def superuser_check(user):
    return user.is_superuser


def force_password_change_check(user):
    return not user.force_password_change


def random_char():
    letters = [i for i in string.ascii_letters]
    letters += [i for i in string.digits]
    return ''.join(random.choices(letters, k=20))


def get_company():
    """getting the correct company"""
    from core.models import Company
    company = Company.objects.filter(active=True).first()
    return company
