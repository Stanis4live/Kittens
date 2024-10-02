from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exhibition.api.v1.views import KittenReadOnlyViewSet, KittenManageViewSet, BreedLListView, RatingCreateView

router = DefaultRouter()

router.register(r'kittens', KittenReadOnlyViewSet, basename='kittens')
router.register(r'manage-kittens', KittenManageViewSet, basename='manage-kittens')


urlpatterns = [
    path('breeds/', BreedLListView.as_view(), name='breed-list'),
    path('rating/', RatingCreateView.as_view(), name='rating-create'),
    path('', include(router.urls)),
]