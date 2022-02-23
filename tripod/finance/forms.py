from django import forms

from finance.models import Invoice


class InvoiceForm(forms.ModelForm):
    """invoice object creation"""
    class Meta:
        model = Invoice
        fields = '__all__'
