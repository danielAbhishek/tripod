from django import forms

from finance.models import Invoice, PaymentHistory, Receipt


class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    """invoice object creation"""

    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceUpdateForm(forms.ModelForm):
    """invoice object update"""

    class Meta:
        model = Invoice
        fields = ['discount', 'full_pay_due_date', 'notes']
        widgets = {'full_pay_due_date': DateInput()}


class PaymentHistoryForm(forms.ModelForm):
    """payment history creation and update"""

    class Meta:
        model = PaymentHistory
        fields = '__all__'
        exclude = ['invoice']
        widgets = {'payment_date': DateInput()}

    def __init__(self, *args, **kwargs):
        self.invoice = kwargs.pop('invoice')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        to_be_paid = self.invoice.to_be_paid()
        if self.instance.payment_amount > to_be_paid:
            raise Exception('Cannot add more than to be paid')
        else:
            return super(PaymentHistoryForm, self).save(*args, **kwargs)


class ReceiptForm(forms.ModelForm):

    class Meta:
        model = Receipt
        fields = '__all__'
        exclude = ['invoice']
