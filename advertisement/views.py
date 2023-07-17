from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (Advertisement, AdvertisementCharacteristic, Category,
                     CategoryCharacteristic, Characteristic)
from .serializers import (AdvertisementCharacteristicSerializer,
                          AdvertisementSerializer,
                          CategoryCharacteristicSerializer, CategorySerializer,
                          CharacteristicSerializer)


class CategoryViewSet(ReadOnlyModelViewSet):
    """Category model viewset"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CharacteristicViewSet(ReadOnlyModelViewSet):
    """Characteristic model viewset"""
    queryset = Characteristic.objects.all()
    serializer_class = CharacteristicSerializer


class CategoryCharacteristicViewSet(ReadOnlyModelViewSet):
    """CategoryCharacteristic model viewset"""
    queryset = CategoryCharacteristic.objects.all()
    serializer_class = CategoryCharacteristicSerializer


class AdvertisementViewSet(ModelViewSet):
    """Advertisement model viewset"""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user =  self.request.GET.get('user')
        if user:
            return Advertisement.objects.filter(author=user)

        return super().get_queryset()


class AdvertisementCharacteristicViewSet(ModelViewSet):
    """AdvertisementCharacteristic model viewset"""
    queryset = AdvertisementCharacteristic.objects.all()
    serializer_class = AdvertisementCharacteristicSerializer
