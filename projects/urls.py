from django.urls import path

from . import views


app_name = 'projects'
urlpatterns = [
    path('', views.ProjectIndexView.as_view(), name='index'),
    path('project/<str:pk>/', views.project_detail, name='detail'),
    path('create-project/', views.createproject, name='create-project'),
    path('update-project/<str:p_uuid>/', views.updateproject, name='update-project'),
    path('delete-project/<str:p_uuid>/', views.deleteproject, name='delete-project'),
]