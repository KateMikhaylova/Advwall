from django.contrib import admin

from .models import Category, Characteristic, CategoryCharacteristic


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
