from rest_framework.serializers import ModelSerializer

from user.models import User


class UserSerializer(ModelSerializer):
    """
    Serializer class to serialize user instances
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'type', 'street', 'city', 'country']

    def validate(self, attrs):
        street = attrs.get('street')
        if street:
            attrs['city'] = street.city
            attrs['country'] = street.city.country
            return attrs
        city = attrs.get('city')
        if city:
            attrs['country'] = city.country
        return attrs

    # TODO add phone number validation with re
