from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from client_user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST'])
def register(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid() is False:
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_serializer.save()
    return Response(data=user_serializer.data, status=status.HTTP_200_OK)


user_view = UserViewSet.as_view({
    'get': 'list',
    'put': 'update',
})
