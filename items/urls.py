from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_item, name='report_item'),
    path('', views.item_list, name='item_list'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('my-items/', views.my_items, name='my_items'),
]