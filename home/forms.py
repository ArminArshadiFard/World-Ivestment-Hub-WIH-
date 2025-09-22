from django import forms
# from captcha.fields import CaptchaField


class ContactForms(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "input-1 text-left my-email-contact", "placeholder": "your email"}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "input-1 text-left my-text-area", "placeholder": "write your text"}))
    # captcha = CaptchaField()

