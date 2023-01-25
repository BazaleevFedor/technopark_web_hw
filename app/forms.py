from django import forms
from django.core.exceptions import ValidationError

from app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20)
    password = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    password = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    username = forms.CharField(min_length=5, max_length=20)

    class Meta:
        model = Profile
        fields = ['email', 'username', 'password']

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_check'):
            raise ValidationError('Passwords do not match!')

        return self.cleaned_data

    def save(self):
        self.cleaned_data.pop('password_check')
        return Profile.objects.create_user(**self.cleaned_data)
