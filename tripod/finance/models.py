from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models


def validate_percentage(value):
    """validate that float value for percentage is between 0, 1"""
    if value > 1 or value < 0:
        raise ValidationError(
            _('%(value) is not within 0,1 range'),
            params={'value': value},
        )


class Invoice(models.Model):
    issue_date = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                null=True,
                                blank=True)
    discount = models.DecimalField(validators=[validate_percentage],
                                   max_digits=3,
                                   decimal_places=2,
                                   null=True,
                                   blank=True)
    total_price = models.DecimalField(max_digits=8,
                                      decimal_places=2,
                                      null=True,
                                      blank=True)
    advance_pay_due_date = models.DateField(null=True, blank=True)
    full_pay_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def get_issue_number(self):
        return str(self.issue_date.strftime("%Y%m%d")) + str(self.id)

    def __str__(self):
        return self.description[:20]

    def get_summary(self):
        pass

    def paid(self):
        ph = self.paymenthistory_set.all()
        if ph:
            return sum([p.payment_amount for p in ph])
        else:
            return 0

    def to_be_paid(self):
        return self.total_price - self.paid()

    def last_paid_date(self):
        ph = self.paymenthistory_set.all()
        if ph:
            return max([p.payment_date for p in ph])
        else:
            return None


class PaymentHistory(models.Model):
    # payment methods
    PAYMENT_METHODS = [('c', 'Cash'), ('cc', 'Credit Card'),
                       ('bt', 'Bank Transfer'), ('ck', 'Cheque'),
                       ('ot', 'Other')]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(max_digits=8,
                                         decimal_places=2,
                                         null=True,
                                         blank=True)
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHODS)

    def diplay_py_methods(self):
        """returning appropriate detail payment methods"""
        return [
            x[1] for x in self.PAYMENT_METHODS if x[0] == self.payment_method
        ][0]


class Receipt(models.Model):
    # STATUSES
    STATUSES = [('paid', 'paid'), ('pend', 'pending'), ('ref', 'refund')]
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    description = models.TextField()
    total_price = models.FloatField()
    total_paid = models.FloatField()
    status = models.CharField(max_length=2)
