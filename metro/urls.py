from django.urls import path
from . import views

app_name = 'metro'

urlpatterns = [
    path('', views.home, name='home'),
]
