from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from core.models import CustomUser
from core.utils import send_code

from job.models import Job

from tripod.ENV import TEMP_PASSWORD
from tripod.utils import random_char


class CustomerCreationForm(forms.ModelForm):
    job_request = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'first_name', 'last_name', 'gender',
            'contact_number', 'city', 'country'
        ]

    def __init__(self, *args, **kwargs):
        self.random_code = random_char()
        super(CustomerCreationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.password = self.random_code
        self.instance.force_password_change = True
        self.instance.password_change_code = self.random_code
        account = CustomUser.objects.create_client(
            email=self.instance.email,
            password=self.instance.password,
            username=self.instance.username,
            first_name=self.instance.first_name,
            last_name=self.instance.last_name,
            gender=self.instance.gender,
            contact_number=self.instance.contact_number,
            city=self.instance.city,
            country=self.instance.country,
            force_password_change=self.instance.force_password_change,
            password_change_code=self.instance.password_change_code)
        print(self.random_code)
        print(self.instance.password)
        print(self.instance.password_change_code)
        send_code(account)
        Job.objects.create(job_name=account.first_name + " request",
                           job_request=self.cleaned_data['job_request'],
                           primary_client=account,
                           status='req')
        return account
