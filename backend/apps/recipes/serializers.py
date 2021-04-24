from rest_framework import serializers
from . import models

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.JSONField()

    class Meta:
        model = models.Recipe
        fields = [
            'ingredients',
            'steps',
        ]
