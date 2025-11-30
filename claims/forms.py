from django import forms
from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['claim_type', 'description', 'contact_method', 'additional_proof']
        widgets = {
            'claim_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the item in detail. Include color, brand, size, distinguishing features, where you lost it, etc.'
            }),
            'contact_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Email: student@school.edu or Phone: 555-1234'
            }),
            'additional_proof': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional: Any additional proof of ownership (receipt number, unique identifiers, etc.)'
            }),
        }
        labels = {
            'claim_type': 'Request Type',
            'description': 'Item Description / Proof of Ownership',
            'contact_method': 'Preferred Contact Method',
            'additional_proof': 'Additional Proof (Optional)',
        }