from django.urls import path
from . import views

urlpatterns = [
    path('process-excel', views.process_excel, name='process_excel'),
]
