from rest_framework import serializers

from .models import Category, Characteristic, CategoryCharacteristic

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', ]


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['id', 'name', ]


class CategoryCharacteristicSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    characteristic = CharacteristicSerializer(read_only=True)

    class Meta:
        model = CategoryCharacteristic
        fields = ['id', 'category', 'characteristic', ]
