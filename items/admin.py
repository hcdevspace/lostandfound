from django.contrib import admin
from .models import Item

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location_found', 'status', 'submitted_by', 'date_found']
    list_filter = ['status', 'category', 'date_found']
    search_fields = ['name', 'description', 'location_found']
    date_hierarchy = 'date_found'