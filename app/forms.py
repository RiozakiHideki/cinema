from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True,
                               min_length=4,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Проверка на уникальность
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

