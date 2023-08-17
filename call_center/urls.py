from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import auth

urlpatterns = [
    path('incoming-calls/', views.get_statistics_of_incoming_calls, name='incoming_calls'),
    path('login/', auth.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
]
