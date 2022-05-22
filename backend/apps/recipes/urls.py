from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('recipes', views.RecipesViewSet)

app_name = 'recipes'

urlpatterns = [
    *router.urls,
]
