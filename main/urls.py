from django.urls import path

from main.apps import MainConfig
from main.views import index, about

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
]