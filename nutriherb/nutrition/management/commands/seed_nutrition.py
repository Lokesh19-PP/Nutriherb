from django.core.management.base import BaseCommand
from nutrition.models import HerbOrFood, HealthIssue, Recipe


class Command(BaseCommand):
    help = 'Seed initial test data for nutrition app'

    def handle(self, *args, **options):
        spinach, _ = HerbOrFood.objects.get_or_create(
            name='Spinach',
            defaults={
                'category': 'Leafy Vegetable',
                'nutrients': 'Iron, Vitamin A, Vitamin C, Folate, Fiber',
                'benefits': 'Supports blood health, immunity, digestion',
            },
        )

        turmeric, _ = HerbOrFood.objects.get_or_create(
            name='Turmeric',
            defaults={
                'category': 'Spice/Herb',
                'nutrients': 'Curcumin, Manganese, Iron',
                'benefits': 'Anti-inflammatory, antioxidant',
            },
        )

        bitter_gourd, _ = HerbOrFood.objects.get_or_create(
            name='Bitter Gourd',
            defaults={
                'category': 'Vegetable',
                'nutrients': 'Vitamin C, Vitamin A, Folate, Fiber',
                'benefits': 'May help regulate blood sugar, supports immunity',
            },
        )

        anemia, _ = HealthIssue.objects.get_or_create(
            name='Anemia',
            defaults={
                'description': 'Low hemoglobin or red blood cells leading to fatigue and weakness.',
            },
        )
        anemia.herbs_or_foods.add(spinach)

        diabetes, _ = HealthIssue.objects.get_or_create(
            name='Diabetes',
            defaults={
                'description': 'High blood sugar levels due to insulin issues.',
            },
        )
        diabetes.herbs_or_foods.add(bitter_gourd, turmeric)

        spinach_dal, _ = Recipe.objects.get_or_create(
            title='Spinach Dal',
            defaults={
                'ingredients': 'Spinach, lentils, onion, tomato, spices, oil, salt',
                'steps': 'Cook lentils. Saute onion and tomato with spices. Add chopped spinach. Combine with lentils and simmer.',
            },
        )
        spinach_dal.herbs_or_foods.add(spinach)

        turmeric_milk, _ = Recipe.objects.get_or_create(
            title='Turmeric Milk',
            defaults={
                'ingredients': 'Milk (or plant milk), turmeric, black pepper, honey',
                'steps': 'Warm milk. Whisk in turmeric and a pinch of black pepper. Sweeten to taste.',
            },
        )
        turmeric_milk.herbs_or_foods.add(turmeric)

        self.stdout.write(self.style.SUCCESS('Seeded nutrition test data.'))



