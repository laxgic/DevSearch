from django.urls import path

from . import views


app_name = 'users'
urlpatterns = [
    path('', views.all_profiles, name='profiles'),
    path('profile/<slug:pk>/', views.single_profile, name='single_profile'),

    # user authentication
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),

    # user account
    path('user_account/', views.user_account, name='user_account'),
    path('edit_account/', views.edit_account, name='edit_account'),

    # user skills
    path('add_skill/', views.add_skill, name='add_skill'),
    path('update_skill/<slug:pk>/', views.update_skill, name='update_skill'),
    path('delete_skill/<slug:pk>/', views.delete_skill, name='delete_skill'),   
]