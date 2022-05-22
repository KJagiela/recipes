from rest_framework import generics

from .models import IngredientCategory
from .serializers import IngredientCategorySerializer


class CategoriesListView(generics.ListAPIView):
    queryset = IngredientCategory.objects.all()
    serializer_class = IngredientCategorySerializer
