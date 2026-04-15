"""
URL configuration for nutriherb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from nutrition.views import (
    HerbOrFoodViewSet,
    HealthIssueViewSet,
    RecipeViewSet,
    recipe_detail_view,
)

router = routers.DefaultRouter()
router.register(r'herbs-foods', HerbOrFoodViewSet, basename='herborsfood')
router.register(r'herbsfoods', HerbOrFoodViewSet, basename='herborsfood_alt')
router.register(r'health-issues', HealthIssueViewSet)
router.register(r'healthissues', HealthIssueViewSet, basename='healthissues_alt')
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('foods/', TemplateView.as_view(template_name='foods.html'), name='foods'),
    path('recipes/', TemplateView.as_view(template_name='recipes.html'), name='recipes'),
    path('recipes/<int:recipe_id>/', recipe_detail_view, name='recipe-detail'),
    path('health/', TemplateView.as_view(template_name='health.html'), name='health'),
]
