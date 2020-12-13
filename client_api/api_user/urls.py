from django.urls import path

from api_user.views import users_list_view, users_detailed_view

urlpatterns = [
    path('', users_list_view, name='api_users_list'),
    path('<pk>', users_detailed_view, name='api_users_detailed')
]