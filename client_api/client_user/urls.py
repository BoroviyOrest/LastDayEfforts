from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from client_user.views import user_view, register

urlpatterns = [
    path('register', register, name='user_register'),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', user_view, name='user_list'),
    path('<pk>', user_view, name='user_detailed'),
]
