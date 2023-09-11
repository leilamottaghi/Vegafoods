from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile,UserAddressModel
from django.contrib.auth.models import User



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'national_id', 'phone_number', 'gender', 'birth_date']



class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddressModel
        fields = ['address', 'city', 'state', 'postal_code']



