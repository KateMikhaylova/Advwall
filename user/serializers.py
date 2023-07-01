from rest_framework.serializers import ModelSerializer
from user.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'type', 'street', 'city', 'country']

    # TODO add phone number validation with re
