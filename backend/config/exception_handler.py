from rest_framework.views import exception_handler

from apps.recipes.views import MissingIngredientsError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, MissingIngredientsError):
        response.data = {'missing_ingredients': exc.missing_ingredients}
    return response
