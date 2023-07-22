from django.contrib import admin

from .models import City, Country, Street


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Class to describe Country model in admin panel"""


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Class to describe City model in admin panel"""


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    """Class to describe Street model in admin panel"""
