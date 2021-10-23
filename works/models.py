from django.db import models

class PlaceInfo(models.Model):
    place_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)

class Food(models.Model):
    photo_hash = models.CharField(max_length=200, unique=True)

class NoFood(models.Model):
    photo_hash = models.CharField(max_length=200, unique=True)