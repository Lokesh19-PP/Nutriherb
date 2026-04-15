from rest_framework import serializers
from .models import HerbOrFood, HealthIssue, Recipe


class HerbOrFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbOrFood
        fields = ['id', 'name', 'category', 'nutrients', 'benefits']


class HealthIssueSerializer(serializers.ModelSerializer):
    herbs_or_foods = serializers.PrimaryKeyRelatedField(
        many=True, queryset=HerbOrFood.objects.all()
    )

    class Meta:
        model = HealthIssue
        fields = ['id', 'name', 'description', 'herbs_or_foods']


class RecipeSerializer(serializers.ModelSerializer):
    herbs_or_foods = serializers.PrimaryKeyRelatedField(
        many=True, queryset=HerbOrFood.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'steps', 'herbs_or_foods']



