from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('recipes/', views.Recipe_Page, name='Recipe_Page'),
    path('recipes/instructions/<int:id>/', views.view_recipes , name='view_recipes'),


     
     
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)