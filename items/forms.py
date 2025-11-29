from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'description', 'location_found', 'date_found', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Blue Water Bottle'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide detailed description of the item'
            }),
            'location_found': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Cafeteria, Gym, Room 1428'
            }),
            'date_found': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'name': 'Item Name',
            'category': 'Category',
            'description': 'Description',
            'location_found': 'Where was it found?',
            'date_found': 'When was it found?',
            'photo': 'Upload Photo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty choice for category
        self.fields['category'].choices = [('', 'Select a category...')] + list(self.fields['category'].choices)[1:]