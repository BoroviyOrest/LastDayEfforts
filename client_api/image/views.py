from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from image.ml_api import MlApiImageRequest
from image.models import RawImage, TransformedImage
from image.serializers import RawImageSerializer, TransformedImageSerializer
from utils.tasks import GetTransformedImage


class UserGalleryView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        raw_images = RawImage.objects.filter(user=request.user)
        transformed_images = TransformedImage.objects.filter(user=request.user)
        raw_images_serializer = RawImageSerializer(raw_images, many=True)
        transformed_images_serializer = TransformedImageSerializer(transformed_images, many=True)

        response_data = {
            'raw_images': raw_images_serializer.data,
            'transformed_images': transformed_images_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class RawImageView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RawImageSerializer
    queryset = RawImage.objects.all()

    def get_queryset(self):
        return self.request.user.raw_images.all()

    def create(self, request, *args, **kwargs):
        image_file = request.data.get('file')
        raw_image_data = {
            'file': image_file,
            'user': request.user.id
        }
        raw_image_serializer = RawImageSerializer(data=raw_image_data)
        if not raw_image_serializer.is_valid():
            return Response(data=raw_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        raw_image_serializer.save()
        return Response(data=raw_image_serializer.data, status=status.HTTP_201_CREATED)


class TransformedImageView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransformedImageSerializer
    queryset = TransformedImage.objects.all()

    def get_queryset(self):
        return self.request.user.transformed_images.all()

    def create(self, request, *args, **kwargs):
        image_id = request.data.get('image')
        if image_id is not None:
            raw_image = RawImage.objects.get(id=image_id, user=request.user.id)
        else:
            return Response(data="{\"error\":Image is missing}", status=status.HTTP_400_BAD_REQUEST)

        style_id = request.data.get('style_id')
        if style_id is None:
            return Response(data="{\"error\":Style code is missing}", status=status.HTTP_400_BAD_REQUEST)

        transform_data = MlApiImageRequest().transform_image(raw_image.file.path, style_id)
        if transform_data is None:
            return Response(data={'details': 'error with api call'}, status=status.HTTP_400_BAD_REQUEST)

        image_data = {
            'style': style_id,
            'user': request.user.id
        }
        new_image_serializer = TransformedImageSerializer(data=image_data)
        if not new_image_serializer.is_valid():
            return Response(data=new_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = new_image_serializer.save()
        GetTransformedImage().delay(transform_data['id'], instance.id)

        return Response(data=new_image_serializer.data, status=status.HTTP_201_CREATED)


gallery_view = UserGalleryView.as_view({
    'get': 'list'
})
raw_image_detailed_view = RawImageView.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})
raw_image_list_view = RawImageView.as_view({
    'post': 'create',
})
transformed_image_detailed_view = TransformedImageView.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})
transformed_image_list_view = TransformedImageView.as_view({
    'post': 'create',
})
