from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import City, Country, Street
from .serializers import CitySerializer, CountrySerializer, StreetSerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class StreetViewSet(ModelViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    
    def get_permissions(self):
        if self.action not in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
