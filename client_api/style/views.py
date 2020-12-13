from requests.exceptions import ConnectionError, Timeout
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from style.ml_api import MlApiStyleRequest


class StyleView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ml_api = MlApiStyleRequest()

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

    def create(self, request):
        description = request.data.get('description')
        if description is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            data = self.ml_api.post(description)
        except (ConnectionError, Timeout) as exc:
            return Response(
                data={'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        description = request.data.get('description')
        if description is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            data = self.ml_api.put(pk, description)
        except (ConnectionError, Timeout) as exc:
            return Response(
                data={'details': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data, status=status.HTTP_200_OK)


styles_detailed_view = StyleView.as_view({
    'get': 'retrieve',
    'put': 'update',
})
styles_list_view = StyleView.as_view({
    'get': 'list',
    'post': 'create',
})
