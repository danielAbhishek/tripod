from core.models import CustomUser, Company
from django import forms
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm)

from tripod.settings import temp_password
from tripod.utils import random_char

from core.utils import send_code

from job.models import Job, JobQuestionnaire

from crispy_forms.helper import FormHelper


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = [
            'password', 'groups', 'user_permissions', 'last_login',
            'date_joined', 'force_password_change', 'password_change_code'
        ]


class StaffProfileUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = [
            'password', 'groups', 'user_permissions', 'last_login',
            'date_joined', 'force_password_change', 'password_change_code',
            'is_staff', 'is_client', 'is_active', 'is_superuser'
        ]


class CustomUserChangeFormAdminView(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = '__all__'


class AccountCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def __init__(self, *args, **kwargs):
        self.password = temp_password
        self.user_type = kwargs.pop('user_type')
        super(AccountCreationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        random_code = random_char()
        if self.user_type == 'client':
            account = CustomUser.objects.create_client(
                self.instance.email,
                random_code,
                username=self.cleaned_data['username'],
                password_change_code=random_code)
        elif self.user_type == 'staff':
            account = CustomUser.objects.create_staff(
                self.cleaned_data['email'],
                random_code,
                self.cleaned_data['username'],
                password_change_code=random_code)
        else:
            raise TypeError(f'Incorrect user type given {self.user_type}')

        send_code(account)
        return account


class JobUserUpdateForm(forms.ModelForm):
    """
    User updating the job details
    """

    class Meta:
        model = Job
        fields = [
            'venue', 'venue_notes', 'start_date', 'end_date', 'start_time',
            'end_time', 'package'
        ]
        widgets = {
            'start_date': DateInput(),
            'start_time': TimeInput(),
            'end_date': DateInput(),
            'end_time': TimeInput(),
        }

    def save(self, *args, **kwargs):
        jobObj = super(JobUserUpdateForm, self).save(*args, **kwargs)
        return jobObj


class JobPackageUpdate(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['package']


class QuestionnaireUpdate(forms.ModelForm):
    """
    User updating answers to question
    """

    class Meta:
        model = JobQuestionnaire
        fields = [
            'answer_one',
            'answer_two',
            'answer_three',
            'answer_four',
            'answer_five',
        ]

    def __init__(self, *args, **kwargs):
        super(QuestionnaireUpdate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class JobReqCreatedForm(forms.ModelForm):
    """
    User creating a job request
    """

    class Meta:
        model = Job
        fields = ['job_name', 'event', 'venue', 'start_date', 'end_date']
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('userObj')
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.create_by = self.user
        self.instance.primary_client = self.user
        self.instance.status = 'req'
        self.instance.created_by = self.user
        jobObj = super(JobReqCreatedForm, self).save(*args, **kwargs)
        return jobObj


class CompanyForm(forms.ModelForm):
    """company model"""

    class Meta:
        model = Company
        fields = '__all__'
        exclude = [
            'active',
        ]
