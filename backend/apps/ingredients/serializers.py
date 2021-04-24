from rest_framework import serializers
from . import models

class IngredientCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IngredientCategory
        fields = {'name'}
