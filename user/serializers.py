from django.core.exceptions import ValidationError
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

        if attrs['street'].city != attrs['city']:
            raise ValidationError('City and street do not correspond')
        if attrs['city'].country != attrs['country']:
            raise ValidationError('Country and city do not correspond')
        return attrs

    # TODO add phone number validation with re
