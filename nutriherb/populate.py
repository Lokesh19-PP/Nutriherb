import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriherb.settings')
django.setup()

from nutrition.models import HerbOrFood, HealthIssue, Recipe

def populate():
    # Adding Foods
    spinach, _ = HerbOrFood.objects.get_or_create(
        name="Spinach", category="food", 
        nutrients="Iron, Vitamin A, Vitamin C, Folate", 
        benefits="Improves blood oxygenation, good for eyes."
    )
    tulsi, _ = HerbOrFood.objects.get_or_create(
        name="Tulsi (Holy Basil)", category="herb",
        nutrients="Vitamin C, Calcium, Zinc, Iron",
        benefits="Boosts immunity, reduces stress, fights infections."
    )
    quinoa, _ = HerbOrFood.objects.get_or_create(
        name="Quinoa", category="food",
        nutrients="Protein, Fiber, Magnesium",
        benefits="Great plant-based protein source."
    )
    turmeric, _ = HerbOrFood.objects.get_or_create(
        name="Turmeric", category="herb",
        nutrients="Curcumin, Manganese, Iron",
        benefits="Strong anti-inflammatory and antioxidant properties."
    )
    ginger, _ = HerbOrFood.objects.get_or_create(
        name="Ginger", category="herb",
        nutrients="Gingerol, Vitamin B3, B6",
        benefits="Aids digestion, reduces nausea."
    )

    # Adding Health Issues
    immunity, _ = HealthIssue.objects.get_or_create(
        name="Low Immunity",
        description="Frequent colds, feelings of lethargy, catching infections easily."
    )
    immunity.herbs_or_foods.add(tulsi, turmeric, ginger)
    
    anemia, _ = HealthIssue.objects.get_or_create(
        name="Anemia / Low Iron",
        description="Fatigue, weakness, pale skin caused by iron deficiency."
    )
    anemia.herbs_or_foods.add(spinach, quinoa)
    
    digestion, _ = HealthIssue.objects.get_or_create(
        name="Poor Digestion",
        description="Bloating, indigestion, acid reflux."
    )
    digestion.herbs_or_foods.add(ginger, tulsi)

    # Adding Recipes
    golden_milk, _ = Recipe.objects.get_or_create(
        title="Golden Milk (Turmeric Latte)",
        ingredients="1 cup milk, 1 tsp turmeric, pinch of black pepper, honey.",
        steps="1. Heat milk. 2. Stir in turmeric and pepper. 3. Simmer for 5 mins. 4. Sweeten with honey."
    )
    golden_milk.herbs_or_foods.add(turmeric)

    spinach_salad, _ = Recipe.objects.get_or_create(
        title="Power Spinach Salad",
        ingredients="2 cups spinach, 1/2 cup cooked quinoa, lemon dressing.",
        steps="1. Mix spinach and quinoa. 2. Add dressing and toss well."
    )
    spinach_salad.herbs_or_foods.add(spinach, quinoa)

    immunity_tea, _ = Recipe.objects.get_or_create(
        title="Tulsi Ginger Tea",
        ingredients="1 cup water, 5 Tulsi leaves, 1 inch crushed ginger.",
        steps="1. Boil water. 2. Add crushed ginger and tulsi. 3. Steep for 5 mins."
    )
    immunity_tea.herbs_or_foods.add(tulsi, ginger)

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
