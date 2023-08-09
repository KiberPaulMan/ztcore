from django.urls import path
from . import views

urlpatterns = [
    path('incoming-calls/', views.get_statistics_of_incoming_calls, name='incoming_calls'),
    path('', views.index, name='index'),
]
