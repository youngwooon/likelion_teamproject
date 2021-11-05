from django.db import models
from django.contrib.auth.models import User

class PlaceInfo(models.Model):
    place_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    vicinity = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)

class Food(models.Model):
    photo_hash = models.CharField(max_length=200, unique=True)

class NoFood(models.Model):
    photo_hash = models.CharField(max_length=200, unique=True)

class PlaceSelected(models.Model):
    name = models.CharField(max_length=50)
    vicinity = models.CharField(max_length=50)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)