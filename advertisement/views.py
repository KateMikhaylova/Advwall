from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Category, Characteristic, CategoryCharacteristic
from .serializers import CategorySerializer, CharacteristicSerializer, CategoryCharacteristicSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class CharacteristicViewSet(ModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer
    
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

class CategoryCharacteristicViewSet(ModelViewSet):
    queryset = CategoryCharacteristic.objects.all()
    serializer_class = CategoryCharacteristicSerializer
    
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
