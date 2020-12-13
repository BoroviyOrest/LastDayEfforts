from requests.exceptions import ConnectionError, Timeout
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api_user.ml_api import MlApiUserRequest


class ApiUserView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ml_api = MlApiUserRequest()

    def retrieve(self, request, pk):
        try:
            data = self.ml_api.retrieve(pk)
        except (ConnectionError, Timeout) as exc:
            return Response(
                data={'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request):
        try:
            data = self.ml_api.list()
        except (ConnectionError, Timeout) as exc:
            return Response(
                data={'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        calls_per_day_limit = request.data.get('calls_per_day_limit')
        is_active = request.data.get('is_active')
        is_admin = request.data.get('is_admin')

        try:
            data = self.ml_api.patch(
                instance_id=pk,
                calls_per_day_limit=calls_per_day_limit,
                is_active=is_active,
                is_admin=is_admin,
            )
        except (ConnectionError, Timeout) as exc:
            return Response(
                data={'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_200_OK)


users_detailed_view = ApiUserView.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})
users_list_view = ApiUserView.as_view({
    'get': 'list',
})
