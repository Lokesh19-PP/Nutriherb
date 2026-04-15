from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from nutrition.views import (
    HerbOrFoodViewSet,
    HealthIssueViewSet,
    RecipeViewSet,
    FavoriteViewSet,
    recipe_detail_view,
    signup_view,
    login_view,
    logout_view,
    profile_view,
)

router = routers.DefaultRouter()
router.register(r'herbsfoods', HerbOrFoodViewSet)
router.register(r'healthissues', HealthIssueViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('foods/', TemplateView.as_view(template_name='foods.html'), name='foods'),
    path('recipes/', TemplateView.as_view(template_name='recipes.html'), name='recipes'),
    path('recipes/<int:recipe_id>/', recipe_detail_view, name='recipe-detail'),
    path('health/', TemplateView.as_view(template_name='health.html'), name='health'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
]
