from django.urls import path
from . import views

# /<str:path_variable_name> 
urlpatterns = [
    path('', views.index, name='list')    
]