from rest_framework import serializers

from .models import City, Country, Street


class CountrySerializer(serializers.ModelSerializer):
    """Country model serializer"""
    class Meta:
        model = Country
        fields = ['id', 'name', ]


class CitySerializer(serializers.ModelSerializer):
    """City model serializer"""
    country = CountrySerializer(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'country', ]


class StreetSerializer(serializers.ModelSerializer):
    """Street model serializer"""
    city = CitySerializer(read_only=True)

    class Meta:
        model = Street
        fields = ['id', 'name', 'city', ]
