from rest_framework import viewsets, permissions, generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from exhibition.models import Kitten, Breed
from exhibition.api.v1.serializers import KittenSerializer, BreedSerializer, RatingSerializer
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


class BreedLListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        kitten = serializer.validated_data['kitten']

        if kitten.owner == self.request.user:
            return Response({'detail:' 'Нельзя ставить оценку своему питомцу'}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(user=self.request.user)





