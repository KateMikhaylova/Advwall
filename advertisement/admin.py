from django.contrib import admin

from .models import Category, Characteristic, CategoryCharacteristic


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    pass

@admin.register(CategoryCharacteristic)
class CategoryCharacteristicAdmin(admin.ModelAdmin):
    pass
