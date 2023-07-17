from rest_framework import serializers

from .models import (Advertisement, AdvertisementCharacteristic, Category,
                     CategoryCharacteristic, Characteristic)


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
    viewed_count = serializers.IntegerField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'name', 'description', 'author', 'category',
                  'adv_characteristics', 'price', 'viewed_count', 'created_at']

    def create(self, validated_data):
        adv_characteristics = validated_data.pop('adv_characteristics')
        validated_data['author'] = self.context.get('request').user

        obj = super().create(validated_data)
        AdvertisementCharacteristic.objects.bulk_create(
            [AdvertisementCharacteristic(advertisement=obj,
                                         characteristic=adv_characteristic.get('characteristic'),
                                         value=adv_characteristic.get('value'))
             for adv_characteristic in adv_characteristics])

        return obj

    def get_author(self, obj):
        """Returns id and username of advertisement's author"""
        return {
            'id': obj.author.id,
            'username': obj.author.username,
        }
