from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from exhibition.models import Kitten
from exhibition.api.v1.serializers import KittenSerializer
from exhibition.api.v1.filtersets import KittenFilterSet


class KittenReadOnlyViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = KittenFilterSet
    pagination_class = LimitOffsetPagination


class KittenManageViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'put', 'patch', 'delete']
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Kitten.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





