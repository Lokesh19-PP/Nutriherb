from django.contrib import admin
from .models import HerbOrFood, HealthIssue, Recipe

@admin.register(HerbOrFood)
class HerbOrFoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category', 'benefits')
    list_filter = ('category',)

@admin.register(HealthIssue)
class HealthIssueAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    filter_horizontal = ('herbs_or_foods',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'ingredients')
    filter_horizontal = ('herbs_or_foods',)
