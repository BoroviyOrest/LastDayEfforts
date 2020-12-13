from datetime import datetime as dt

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from image.models import TransformedImage
from image.serializers import TransformedImageSerializer
from statistics.ml_api import MlApiStatsRequest
from utils.dataset import format_api_dataset, format_client_dataset


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_client_users_stats(request):
    user_id = request.query_params.get('user_id')
    style_id = request.query_params.get('style_id')
    from_datetime = request.query_params.get('from_datetime')
    to_datetime = request.query_params.get('to_datetime')

    filter_data = {}
    if user_id is not None:
        filter_data['user_id'] = user_id
    if style_id is not None:
        filter_data['style'] = style_id
    if from_datetime is not None:
        filter_data['created_on__gte'] = dt.fromisoformat(from_datetime)
    if to_datetime is not None:
        filter_data['created_on__lt'] = dt.fromisoformat(to_datetime)

    images = TransformedImage.objects.filter(**filter_data)
    serialized_images = [TransformedImageSerializer(image).data for image in images]

    dataset = []
    if len(serialized_images) > 0:
        dataset = format_client_dataset(serialized_images)

    return Response(dataset, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_api_users_stats(request):
    user_uuid = request.query_params.get('user_uuid')
    style_id = request.query_params.get('style_id')
    from_datetime = request.query_params.get('from_datetime')
    to_datetime = request.query_params.get('to_datetime')

    data = MlApiStatsRequest().filter(
        user_uuid=user_uuid,
        style_id=style_id,
        from_datetime=from_datetime,
        to_datetime=to_datetime
    )
    dataset = []
    if len(data) > 0:
        dataset = format_api_dataset(data)

    return Response(dataset, status=status.HTTP_200_OK)
