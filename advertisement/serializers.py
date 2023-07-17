from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (Advertisement, AdvertisementCharacteristic, Category,
                     CategoryCharacteristic, Characteristic)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Country model serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', ]


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer"""
    class Meta:
        model = Category
        fields = ['id', 'name', ]


class CharacteristicSerializer(serializers.ModelSerializer):
    """Characteristic model serializer"""
    class Meta:
        model = Characteristic
        fields = ['id', 'name', ]


class CategoryCharacteristicSerializer(serializers.ModelSerializer):
    """CategoryCharacteristic model serializer"""
    category = CategorySerializer(read_only=True)
    characteristic = CharacteristicSerializer(read_only=True)

    class Meta:
        model = CategoryCharacteristic
        fields = ['id', 'category', 'characteristic', ]


class AdvertisementCharacteristicSerializer(serializers.ModelSerializer):
    """AdvertisementCharacteristic model serializer"""
    class Meta:
        model = AdvertisementCharacteristic
        fields = ['characteristic', 'value']


class AdvertisementSerializer(serializers.ModelSerializer):
    """Advertisement model serializer"""
    adv_characteristics = AdvertisementCharacteristicSerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'name', 'description', 'author', 'category',
                  'adv_characteristics', 'price', 'viewed_count', 'created_at']
