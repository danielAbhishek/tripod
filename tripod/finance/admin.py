from django.contrib import admin

from finance.models import Invoice, PaymentHistory, Receipt


admin.site.register(Invoice)
admin.site.register(PaymentHistory)
admin.site.register(Receipt)
