from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/', views.Recipe_Page, name='Recipe_Page'),

     
     
]