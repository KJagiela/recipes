from django.conf import settings
from django.db import models

from django_extensions.db.models import TimeStampedModel


class Recipe(TimeStampedModel):
    ingredients = models.ManyToManyField('recipes.Ingredient', through='recipes.RecipeIngredient')
    steps = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('recipes.Ingredient', on_delete=models.PROTECT)
    unit = models.CharField(max_length=50)  # TODO: maybe model or enum?
    # TODO: dynamiczne przeliczanie kg<->g etc
    amount = models.DecimalField(max_digits=5, decimal_places=2)


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey('recipes.IngredientCategory', on_delete=models.PROTECT)


class IngredientCategory(models.Model):
    name = models.CharField(max_length=50)
