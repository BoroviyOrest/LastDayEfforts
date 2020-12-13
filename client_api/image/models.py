from django.contrib.auth.models import User
from django.db import models


class RawImage(models.Model):
    file = models.ImageField(upload_to='data/raw_images/')
    name = models.CharField(max_length=20, default='Raw image')
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='raw_images', on_delete=models.CASCADE)


class TransformedImage(models.Model):
    file = models.ImageField(upload_to='data/transformed_images/', null=True)
    name = models.CharField(max_length=20, default='Transformed image')
    created_on = models.DateTimeField(auto_now_add=True)
    style = models.SmallIntegerField()
    user = models.ForeignKey(User, related_name='transformed_images', on_delete=models.CASCADE)
