from django import forms

class regForm(forms.Form):
    name = forms.CharField(max_length=12)
    password = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=80)
    sex = forms.CharField(max_length=1)
    checknumber = forms.CharField(max_length=4)

class loginForm(forms.Form):
    name = forms.CharField(max_length=12)
    password = forms.CharField(max_length=30)
    remember = forms.BooleanField(required=False)
    checknumber = forms.CharField(max_length=4)