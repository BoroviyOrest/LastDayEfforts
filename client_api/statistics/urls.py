from django.urls import path

from statistics.views import get_api_users_stats, get_client_users_stats

urlpatterns = [
    path('api_users', get_api_users_stats, name='api_users_stats'),
    path('client_users', get_client_users_stats, name='client_users_stats')
]