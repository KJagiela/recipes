from django.db import models

from django_extensions.db.models import TimeStampedModel


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        'ingredients.IngredientCategory',
        on_delete=models.PROTECT,
    )


class IngredientCategory(models.Model):
    name = models.CharField(max_length=50)
