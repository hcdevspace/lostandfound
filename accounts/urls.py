from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]