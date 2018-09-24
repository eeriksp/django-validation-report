from django.urls import path
from . import views

urlpatterns = [
    path('', views.validation_report, name='validation-report'),
]