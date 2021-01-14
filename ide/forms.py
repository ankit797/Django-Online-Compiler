
from django import forms
from django.contrib.auth.models import User
from ide.models import userprofile,savecode

class AddCode(forms.ModelForm):

    # this is only for print help_text on placeholder of input
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text

    class Meta:
        model = savecode
        fields = ['language','code']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name']


class DateInput(forms.DateInput):
    input_type = 'date'


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget =DateInput())

    class Meta:
        model = userprofile
        fields = ['phone_number','date_of_birth' ,'gender' , 'profile_photo', 'bio']