from django.urls import path
from . import views

urlpatterns = [
    path('<int:item_pk>/submit/', views.submit_claim, name='submit_claim'),
    path('<int:item_pk>/submit/<str:claim_type>/', views.submit_claim, name='submit_claim_typed'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('admin/', views.admin_claims, name='admin_claims'),
    path('admin/<int:claim_pk>/review/', views.review_claim, name='review_claim'),
]