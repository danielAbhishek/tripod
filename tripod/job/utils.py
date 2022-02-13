from core.models import Company


def get_company():
    """getting the correct company"""
    company = Company.objects.all().first()
    return company
