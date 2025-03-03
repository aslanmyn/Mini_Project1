from django import forms
from .models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['address', 'phone_number', 'email', 'profile_picture', 'username']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user





    
    
