from rest_framework.routers import DefaultRouter

from .views import CityViewSet, CountryViewSet, StreetViewSet

app_name = 'address'

router = DefaultRouter()
router.register('countries', CountryViewSet, basename='countries')
router.register('cities', CityViewSet, basename='cities')
router.register('streets', StreetViewSet, basename='streets')

urlpatterns = router.urls
