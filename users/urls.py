from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('', views.all_profiles, name='profiles'),
    path('profile/<slug:pk>/', views.single_profile, name='single_profile'),
]