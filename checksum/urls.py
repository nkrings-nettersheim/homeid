from django.urls import path
from . import views

app_name = 'checksum'

urlpatterns = [
    path('', views.homeid, name='homeid'),
]
