from django.contrib import admin

from .models import (Advertisement, AdvertisementCharacteristic, Category,
                     CategoryCharacteristic, Characteristic)


class CategoryCharacteristicInline(admin.TabularInline):
    """Class to describe inlines for Category model in admin panel"""
    model = CategoryCharacteristic
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class to describe Category model in admin panel"""
    inlines = [CategoryCharacteristicInline, ]


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    """Class to describe Characteristic model in admin panel"""


@admin.register(CategoryCharacteristic)
class CategoryCharacteristicAdmin(admin.ModelAdmin):
    """Class to describe CategoryCharacteristic model in admin panel"""


class AdvertisementCharacteristicInline(admin.TabularInline):
    """Class to describe inlines for Advertisement model in admin panel"""
    model = AdvertisementCharacteristic
    extra = 3


@admin.register(AdvertisementCharacteristic)
class AdvertisementCharacteristicAdmin(admin.ModelAdmin):
    """Class to describe AdvertisementCharacteristic model in admin panel"""


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Class to describe Advertisement model in admin panel"""
    inlines = [AdvertisementCharacteristicInline, ]
