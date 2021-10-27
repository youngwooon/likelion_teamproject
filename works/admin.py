from django.contrib import admin
from works.models import PlaceInfo, Food, NoFood, PlaceSelected

@admin.register(PlaceInfo)
class PlaceInfoAdmin(admin.ModelAdmin):
    list_display = ['place_id', 'name', 'lat', 'lng']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['photo_hash']

@admin.register(NoFood)
class NoFoodAdmin(admin.ModelAdmin):
    list_display = ['photo_hash']

@admin.register(PlaceSelected)
class PlaceSelectedAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']