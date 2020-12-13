from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        is_banned = validated_data.get('is_banned')

        if is_banned is not None and is_banned is not instance.is_active:
            instance.is_active = is_banned
            instance.save()
        return instance
