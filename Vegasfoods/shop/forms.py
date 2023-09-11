from django import forms
from .models import ContactModel

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'نام',
            'email': 'ایمیل',
            'subject': 'موضوع',
            'message': 'پیام'
        }
     
