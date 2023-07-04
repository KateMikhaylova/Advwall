from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CharacteristicViewSet, CategoryCharacteristicViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('characteristics', CharacteristicViewSet, basename='characteristics')
router.register('cat_characteristics', CategoryCharacteristicViewSet, basename='cat_characteristics')

urlpatterns = router.urls