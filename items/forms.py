from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
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
                'type': 'date',
                'max': timezone.now().date().isoformat()
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp'
            })
        }
        labels = {
            'name': 'Item Name',
            'category': 'Category',
            'description': 'Description',
            'location_found': 'Where was it found?',
            'date_found': 'When was it found?',
            'photo': 'Upload Photo (Max 5MB, JPG/PNG/GIF/WEBP only)'
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        # Add empty choice for category
        self.fields['category'].choices = [('', 'Select a category...')] + list(Item.CATEGORY_CHOICES)
        self.fields['photo'].required = not (instance and getattr(instance, 'pk', None))
        # Set max date to today for date_found field
        self.fields['date_found'].widget.attrs['max'] = timezone.now().date().isoformat()

    def clean_date_found(self):
        date_found = self.cleaned_data.get('date_found')
        if date_found and date_found > timezone.now().date():
            raise forms.ValidationError('The date found cannot be in the future.')
        return date_found

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        
        if photo:
            # Check file size (5MB = 5 * 1024 * 1024 bytes)
            max_size = 5 * 1024 * 1024  # 5MB
            if photo.size > max_size:
                raise ValidationError('Image file size cannot exceed 5MB.')
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
            content_type = photo.content_type
            
            if content_type not in allowed_types:
                raise ValidationError('Only JPG, PNG, GIF, and WEBP image files are allowed.')
            
            # Additional check for file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            file_name = photo.name.lower()
            
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise ValidationError('Only JPG, PNG, GIF, and WEBP image files are allowed.')
        
        return photo