import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nutriherb.settings')
django.setup()

from nutrition.models import HerbOrFood

def add_spices():
    spices = [
        {
            "name": "Cinnamon",
            "category": "spice",
            "nutrients": "Cinnamaldehyde, Fiber, Manganese",
            "benefits": "Helps manage blood sugar levels and has powerful anti-diabetic effects."
        },
        {
            "name": "Clove",
            "category": "spice",
            "nutrients": "Eugenol, Vitamin K, Manganese",
            "benefits": "Strong antimicrobial properties and excellent for oral health."
        },
        {
            "name": "Black Pepper",
            "category": "spice",
            "nutrients": "Piperine, Iron, Vitamin K",
            "benefits": "Enhances nutrient absorption (especially curcumin) and improves digestion."
        },
        {
            "name": "Cardamom",
            "category": "spice",
            "nutrients": "Antioxidants, Vitamin C, Magnesium",
            "benefits": "Improves heart health and helps with digestive issues."
        },
        {
            "name": "Cumin",
            "category": "spice",
            "nutrients": "Iron, Flavonoids, Essential Oils",
            "benefits": "Promotes digestion and reduces food-borne infections."
        }
    ]

    for spice_data in spices:
        spice, created = HerbOrFood.objects.get_or_create(
            name=spice_data["name"],
            defaults={
                "category": spice_data["category"],
                "nutrients": spice_data["nutrients"],
                "benefits": spice_data["benefits"]
            }
        )
        if created:
            print(f"Added spice: {spice.name}")
        else:
            print(f"Spice already exists: {spice.name}")

if __name__ == '__main__':
    add_spices()
