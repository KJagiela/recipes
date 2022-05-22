from django.conf import settings
from django.db import models

from django_extensions.db.models import TimeStampedModel


class AvailableLanguages(models.IntegerChoices):
    ENGLISH = 1
    POLISH = 2


class Recipe(TimeStampedModel):
    ingredients = models.ManyToManyField(
        'ingredients.Ingredient',
        through='recipes.RecipeIngredient',
    )
    steps = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.IntegerField(
        choices=AvailableLanguages.choices,
        default=AvailableLanguages.POLISH,
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('ingredients.Ingredient', on_delete=models.PROTECT)
    unit = models.CharField(max_length=50)  # TODO: maybe model or enum?
    # TODO: dynamically convert to grams
    amount = models.DecimalField(max_digits=5, decimal_places=2)
