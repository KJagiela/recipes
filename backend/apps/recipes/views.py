from rest_framework import viewsets, exceptions, status, generics

from .models import Recipe, Ingredient, RecipeIngredient
from .serializers import RecipeSerializer
# TODO: get recipe by link
# TODO: get recipe by direct post
# TODO get recipe from a photo


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
        for ingredient in ingredients:
            try:
                ingr_object = Ingredient.objects.get(name=ingredient['name'].lower())
            except Ingredient.DoesNotExist:
                # todo: AI to create category if not exists (user confirmation required)
                missing_ingredients.append(ingredient['name'].lower())
                continue
            # todo translate ingredients from polish to english
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingr_object,
                amount=ingredients['amount'],
                unit=ingredients['unit'],
            )
        if missing_ingredients:
            raise MissingIngredientsError(missing_ingredients)
        recipe.save()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoriesListView(generics.ListView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer