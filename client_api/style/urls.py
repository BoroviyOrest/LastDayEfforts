from django.urls import path

from style.views import styles_detailed_view, styles_list_view

urlpatterns = [
    path('', styles_list_view, name='style_list'),
    path('<pk>', styles_detailed_view, name='style_detailed')
]
