from django.contrib import admin

from .models import (Advertisement, AdvertisementCharacteristic, Category,
                     CategoryCharacteristic, Characteristic)


class CategoryCharacteristicInline(admin.TabularInline):
    model = CategoryCharacteristic
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryCharacteristicInline, ]


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryCharacteristic)
class CategoryCharacteristicAdmin(admin.ModelAdmin):
    pass


class AdvertisementCharacteristicInline(admin.TabularInline):
    model = AdvertisementCharacteristic
    extra = 3


@admin.register(AdvertisementCharacteristic)
class AdvertisementCharacteristicAdmin(admin.ModelAdmin):
    pass

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [AdvertisementCharacteristicInline, ]
