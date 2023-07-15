from django.contrib import admin

from .models import City, Country, Street


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    pass
