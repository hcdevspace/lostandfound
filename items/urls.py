from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_item, name='report_item'),
    path('', views.item_list, name='item_list'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('my-items/', views.my_items, name='my_items'),
]