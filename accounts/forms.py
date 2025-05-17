from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'})
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'})
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'style': 'background:#414868; color:#fff; border:none;'})
        } 