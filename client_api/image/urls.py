from django.urls import path

from image.views import (
    raw_image_list_view,
    raw_image_detailed_view,
    transformed_image_list_view,
    transformed_image_detailed_view,
    gallery_view
)

urlpatterns = [
    path('raw/', raw_image_list_view, name='raw_images_list'),
    path('raw/<pk>', raw_image_detailed_view, name='raw_images'),
    path('transformed/', transformed_image_list_view, name='transformed_images_list'),
    path('transformed/<pk>', transformed_image_detailed_view, name='transformed_images'),
    path('gallery/', gallery_view, name='gallery'),
]
