from django.urls import path, include

urlpatterns = [
    path('api/api_user/', include('api_user.urls')),
    path('api/user/', include('client_user.urls')),
    path('api/image/', include('image.urls')),
    path('api/style/', include('style.urls')),
    path('api/stats/', include('statistics.urls')),
]
