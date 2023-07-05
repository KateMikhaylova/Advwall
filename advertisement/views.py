from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .models import Category, Characteristic, CategoryCharacteristic, Advertisement, AdvertisementCharacteristic
from .serializers import CategorySerializer, CharacteristicSerializer, CategoryCharacteristicSerializer, AdvertisementSerializer, AdvertisementCharacteristicSerializer
from .mixins import UserQuerySetMixin


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CharacteristicViewSet(ReadOnlyModelViewSet):
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer
    

class CategoryCharacteristicViewSet(ReadOnlyModelViewSet):
    queryset = CategoryCharacteristic.objects.all()
    serializer_class = CategoryCharacteristicSerializer


class AdvertisementViewSet(UserQuerySetMixin,
                           ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    user_field = 'author'
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, viewed_count=0)
    

class AdvertisementCharacteristicViewSet(ModelViewSet):
    queryset = AdvertisementCharacteristic.objects.all()
    serializer_class = AdvertisementCharacteristicSerializer
