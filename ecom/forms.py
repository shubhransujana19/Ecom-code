from django.contrib.auth.forms import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Customer

#User Registration Form
class MyRegForm(UserCreationForm):
    username=forms.CharField(label="Enter username", widget=forms.TextInput(
        attrs={'placeholder':"Enter username", 'class':'form-control border-primary'}))
    first_name = forms.CharField(label="Enter your First Name", widget=forms.TextInput(
        attrs={'placeholder': "Enter your First Name", 'class': 'form-control border-primary'}))
    last_name = forms.CharField(label="Enter your Last Name", widget=forms.TextInput(
        attrs={'placeholder': "Enter your Last Name", 'class': 'form-control border-primary'}))
    email = forms.CharField(label="Enter your email", widget=forms.EmailInput(
        attrs={'placeholder': "Enter your email", 'class': 'form-control border-primary'}))
    password1 = forms.CharField(label="Enter your password", widget=forms.PasswordInput(
        attrs={'placeholder': "Enter your password", 'class': 'form-control border-primary'}))
    password2 = forms.CharField(label="Enter your confirm password", widget=forms.PasswordInput(
        attrs={'placeholder': "Enter your confirm password", 'class': 'form-control border-primary'}))
    class Meta:
        model=User
        fields=['username','first_name', 'last_name', 'email','password1','password2']       

#User Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Enter username", widget=forms.TextInput(
        attrs={'placeholder': "Enter username", 'class': 'form-control border-primary'}))
    password = forms.CharField(label="Enter your password", widget=forms.PasswordInput(
        attrs={'placeholder': "Enter your password", 'class': 'form-control border-primary'}))

class ChangeProfileForm(UserChangeForm):
    password = None
    first_name = forms.CharField(label="Your First Name", widget=forms.TextInput(
        attrs={'placeholder': "Your First Name", 'class': 'form-control border-primary'}))
    last_name = forms.CharField(label="Your Last Name", widget=forms.TextInput(
        attrs={'placeholder': "Your Last Name", 'class': 'form-control border-primary'}))
    email = forms.CharField(label="Your email", widget=forms.EmailInput(
        attrs={'placeholder': "Your email", 'class': 'form-control border-primary'}))
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'email']

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Enter your current password", widget=forms.PasswordInput(
        attrs={'placeholder': "Enter your current password", 'class': 'form-control border-primary'}))
    new_password1 = forms.CharField(label="Enter your new password", widget=forms.PasswordInput(
        attrs={'placeholder': "Enter your new password", 'class': 'form-control border-primary'}))
    new_password2 = forms.CharField(label="Enter your confirm password", widget=forms.PasswordInput(
        attrs={'placeholder': "Enter your confirm password", 'class': 'form-control border-primary'}))
