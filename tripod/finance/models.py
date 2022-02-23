
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from job.models import Job


def validate_percentage(value):
    """validate that float value for percentage is between 0, 1"""
    if value > 1 or value < 0:
        raise ValidationError(
            _('%(value) is not within 0,1 range'),
            params={'value': value},
        )


class Invoice(models.Model):
    issue_date = models.DateTimeField(auto_now=True)
    job = models.OneToOneField(
        Job, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(
        validators=[validate_percentage],
        max_digits=3, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(null=True, blank=True)

    def get_issue_number(self):
        return str(self.issue_date)+str(self.id)


class PaymentHistory(models.Model):
    # payment methods
    PAYMENT_METHODS = [
        ('c', 'Cash'),
        ('cc', 'Credit Card'),
        ('bt', 'Bank Transfer'),
        ('ck', 'Cheque'),
        ('ot', 'Other')
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHODS)


class Receipt(models.Model):
    # STATUSES
    STATUSES = [
        ('paid', 'paid'),
        ('pend', 'pending'),
        ('ref', 'refund')
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.TextField()
    total_price = models.FloatField()
    total_paid = models.FloatField()
    status = models.CharField(max_length=2)
