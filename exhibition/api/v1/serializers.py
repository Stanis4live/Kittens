from rest_framework import serializers
from exhibition.models import Kitten, Breed, Rating

class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ['id', 'owner', 'breed', 'color', 'age_months', 'description']
        read_only_fields = ['id', 'owner']


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']
        read_only_fields = ['id']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'kitten', 'user', 'score']
        read_only_fields = ['id', 'user']

    def validate_kitten(self, value):
        req = self.context.get('request')
        if req.user == value.owner:
            raise serializers.ValidationError('Нельзя ставить оценку своему питомцу')
        return value
