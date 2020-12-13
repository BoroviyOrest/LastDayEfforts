from rest_framework import serializers

from image.models import RawImage, TransformedImage


class RawImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawImage
        fields = ('id', 'file', 'name', 'created_on', 'user')
        read_only_fields = ['id', 'created_on']


class TransformedImageSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = TransformedImage
        fields = ('id', 'file', 'name', 'created_on', 'style', 'user')
        read_only_fields = ['id', 'created_on']
