from rest_framework import serializers

from .models import Category, Characteristic, CategoryCharacteristic, Advertisement, AdvertisementCharacteristic


class UserSerializer(serializers.ModelSerializer):
    pass


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


class AdvertisementSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'name', 'description', 'author', 'category',
                  'price', 'viewed_count', 'created_at']


class AdvertisementCharacteristicSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(read_only=True)
    characteristic = CharacteristicSerializer(read_only=True)

    class Meta:
        model = AdvertisementCharacteristic
        fields = ['id', 'advertisement', 'characteristic', 'value']
