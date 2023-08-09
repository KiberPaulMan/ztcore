from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('incoming-calls/', csrf_exempt(views.get_statistics_of_incoming_calls), name='incoming_calls'),
    path('', views.index, name='index'),
]
