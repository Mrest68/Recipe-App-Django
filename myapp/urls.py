from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path('', views.Landing_Page, name="LandingPage"),
    path('UserInputForm', views.UserInputForm, name="userinputform"),
    path('recipes/', views.Recipe_Page, name='Recipe_Page'),
    path('recipes/addMeal/', views.add_meal, name="addMeal"),
    path('delete_meal/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('recipes/morerecipes', views.MoreRecipes, name = 'morerecipes')

]
