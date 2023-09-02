from urllib import request

from django import forms
from django.core.exceptions import ValidationError
from django.contrib import auth
from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20)
    password = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    password = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    username = forms.CharField(min_length=5, max_length=20)
    avatar = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['email', 'username', 'password', 'avatar']

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_check'):
            raise ValidationError('Passwords do not match!')

        return self.cleaned_data

    def save(self):
        self.cleaned_data.pop('password_check')
        profile = Profile.objects.create_user(**self.cleaned_data)
        profile.avatar = self.cleaned_data['avatar']
        return profile


class SettingsForm(forms.ModelForm):
    #old_password_check = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    #password_check = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    #password = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
    username = forms.CharField(min_length=5, max_length=20)
    avatar = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['email', 'username', 'avatar']

    def clean(self):
        #if self.cleaned_data.get('password') != self.cleaned_data.get('password_check'):
            #raise ValidationError('Passwords do not match!')

        return self.cleaned_data

    def save(self):
        profile = Profile.objects.get(self)
        profile.avatar = self.cleaned_data['avatar']
        profile.email = self.cleaned_data['email']
        profile.username = self.cleaned_data['username']
        profile.save()
        return profile

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', 'profile']

