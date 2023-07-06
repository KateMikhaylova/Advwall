from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import City, Country, Street
from .serializers import CitySerializer, CountrySerializer, StreetSerializer


class CountryViewSet(ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, ]


class CityViewSet(ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, ]


class StreetViewSet(ReadOnlyModelViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    permission_classes = [IsAuthenticated, ]
