from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=32)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='Password', widget=forms.PasswordInput)