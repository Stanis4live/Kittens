from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exhibition.api.v1.views import KittenReadOnlyViewSet, KittenManageViewSet

router = DefaultRouter()

router.register(r'kittens', KittenReadOnlyViewSet, basename='kittens')
router.register(r'manage-kittens', KittenManageViewSet, basename='manage-kittens')


urlpatterns = [
    path('', include(router.urls)),
]