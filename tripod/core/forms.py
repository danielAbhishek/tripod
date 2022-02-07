from core.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['password', 'groups', 'user_permissions', 'last_login']


class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop('password')
        self.user_type = kwargs.pop('user_type')
        super(AccountCreationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.password = self.password
        if self.user_type == 'client':
            account = CustomUser.objects.create_client(
                self.instance.email,
                self.instance.password
            )
        elif self.user_type == 'staff':
            account = CustomUser.objects.create_staff(
                self.cleaned_data['email'],
                self.instance.password,
                self.cleaned_data['username'],
            )
        else:
            raise TypeError(f'Incorrect user type given {self.user_type}')

        return account
