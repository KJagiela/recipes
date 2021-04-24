from rest_framework import viewsets, exceptions, status, generics

from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer
# TODO: get recipe by link
# TODO: get recipe by direct post
# TODO get recipe from a photo
from apps.ingredients.models import Ingredient


class MissingIngredientsError(exceptions.APIException):
    status_code = status.HTTP_428_PRECONDITION_REQUIRED
    def __init__(self, missing_ingredients, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.missing_ingredients = missing_ingredients


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        ingredients = serializer.validated_data.pop('ingredients')
        recipe = Recipe(
            owner=self.request.user,
            **serializer.validated_data,
        )
        missing_ingredients = []
        for ingredient_candidate in ingredients:
            ingredient_name = ingredient_candidate['name'].lower()
            try:
                ingredient = Ingredient.objects.get(name=ingredient_name)
            except Ingredient.DoesNotExist:
                # todo: AI to create category if not exists (user confirmation required)
                missing_ingredients.append(ingredient_candidate['name'].lower())
                continue
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredients['amount'],
                unit=ingredients['unit'],
            )
        if missing_ingredients:
            raise MissingIngredientsError(missing_ingredients)
        recipe.save()
