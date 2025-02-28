from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Contact, Feedback


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'email']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['feedback']


# main_app/forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
