from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ingredients'

router = DefaultRouter()
router.register('ingredients', views.RecipesViewSet)


urlpatterns = [
    *router.urls,
]
