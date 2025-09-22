from django import forms
from django.contrib.auth.models import User
# from captcha.fields import CaptchaField


class RegisterForms(forms.Form):
    def clean(self):
        super(RegisterForms, self).clean()

    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "input-1 my_input", "placeholder": "email"}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-1 my_input", "placeholder": "name"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input-1 my_input", "placeholder": "password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input-1 my_input", "placeholder": "confirm password"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(username=email)
        if qs.exists():
            self.add_error("email", "The entered email is registered before")
        return email

    def clean_password2(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            self.add_error("password", "Passwords are inconsistent")
        if not 7 < int(len(password)) < 20:
            self.add_error("password", "Passwords length is not valid")
        return data


class LoginForms(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "input-1 my_input", "placeholder": "your email"}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input-1 my_input", "placeholder": "password"}))

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     qs = User.objects.filter(username=email)
    #     if not qs.exists():
    #         self.add_error("password", "The entered email is not registered before")
    #     return email


# class CaptchaTestForm(forms.Form):
#     myfield = forms.CharField()
#     captcha = CaptchaField()
