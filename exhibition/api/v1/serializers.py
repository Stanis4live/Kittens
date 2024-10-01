from rest_framework import serializers
from exhibition.models import Kitten

class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ['id', 'owner', 'breed', 'color', 'age_months', 'description']
        read_only_fields = ['id', 'owner']