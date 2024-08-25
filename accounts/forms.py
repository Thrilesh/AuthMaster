from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class userRegisterform(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Username'
            elif field_name in ['password1', 'password2']:
                field.widget.attrs['placeholder'] = 'Password'


class userLoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=64, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter old password'}))
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))

    class Meta:
        model = User
        fields = ['password1', 'password2']
