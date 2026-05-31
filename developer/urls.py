from django.urls import path
from . import views

urlpatterns = [
    path('api/snapshot/', views.snapshot, name='dev_snapshot'),
    path('api/save/', views.save_instructions, name='dev_save'),
    path('api/begin-recording/', views.begin_recording, name='dev_begin_recording'),
    path('api/relogin/', views.relogin, name='dev_relogin'),
    path('api/load-snapshot/', views.load_snapshot, name='dev_load_snapshot'),
    path('api/instructions/', views.get_instructions, name='dev_get_instructions'),
    path('simulate/', views.simulate_home, name='dev_simulate'),
]
