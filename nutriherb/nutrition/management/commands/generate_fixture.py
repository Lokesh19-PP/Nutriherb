import json
import os
import random
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate a Django fixture sample_data.json with >=1000 records (HerbOrFood, HealthIssue, Recipe)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="nutrition/fixtures/sample_data.json",
            help="Output path for the generated fixture (relative to project root)",
        )
        parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
        parser.add_argument("--foods", type=int, default=650, help="Target number of HerbOrFood records")
        parser.add_argument("--issues", type=int, default=60, help="Target number of HealthIssue records")
        parser.add_argument("--recipes", type=int, default=400, help="Target number of Recipe records")

    def handle(self, *args, **options):
        random.seed(options["seed"])

        base_dir = Path(__file__).resolve().parents[3]  # project root (contains manage.py)
        output_rel = options["output"]
        output_path = base_dir / output_rel

        # Ensure fixtures directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fixture = []

        # ---------- Data sources ----------
        herb_names = [
            "Turmeric", "Tulsi", "Neem", "Ashwagandha", "Moringa", "Curry Leaves", "Fenugreek",
            "Ginger", "Garlic", "Clove", "Cardamom", "Cinnamon", "Black Pepper", "Fennel",
            "Coriander", "Mint", "Basil", "Thyme", "Oregano", "Rosemary", "Sage", "Chamomile",
        ]
        food_names = [
            "Spinach", "Kale", "Beetroot", "Carrot", "Tomato", "Onion", "Potato", "Sweet Potato",
            "Bitter Gourd", "Bottle Gourd", "Cabbage", "Cauliflower", "Broccoli", "Green Peas",
            "Cucumber", "Pumpkin", "Eggplant", "Okra", "Mushroom", "Zucchini", "Capsicum",
            "Apple", "Banana", "Papaya", "Mango", "Orange", "Lemon", "Guava", "Pomegranate",
            "Blueberries", "Strawberries", "Avocado", "Grapes", "Watermelon", "Pineapple",
            "Oats", "Brown Rice", "Quinoa", "Bajra", "Jowar", "Ragi", "Wheat", "Barley",
            "Chickpeas", "Kidney Beans", "Lentils", "Moong Dal", "Black Gram", "Green Gram",
            "Almonds", "Walnuts", "Cashews", "Pistachios", "Flaxseeds", "Chia Seeds", "Sesame",
            "Milk", "Yogurt", "Paneer", "Ghee", "Cheese", "Eggs", "Chicken", "Fish", "Salmon",
        ]
        extra_pool = [
            "Pear", "Peach", "Plum", "Apricot", "Kiwi", "Dragon Fruit", "Lychee", "Dates", "Figs",
            "Cranberries", "Blackberries", "Raspberries", "Corn", "Sorghum", "Amaranth", "Buckwheat",
            "Sunflower Seeds", "Pumpkin Seeds", "Hazelnuts", "Macadamia", "Brazil Nuts",
            "Cottage Cheese", "Tofu", "Tempeh", "Edamame", "Seaweed", "Nori", "Kombu",
            "Coconut", "Coconut Water", "Coconut Milk", "Green Tea", "Black Tea",
        ]

        nutrient_pool = [
            "Iron", "Vitamin C", "Vitamin A", "Vitamin E", "Vitamin K", "Folate", "Calcium",
            "Magnesium", "Potassium", "Zinc", "Selenium", "Protein", "Omega-3", "Fiber",
            "Antioxidants", "Manganese", "Copper", "B Vitamins",
        ]
        benefit_phrases = [
            "Boosts immunity", "Improves digestion", "Supports heart health", "Lowers blood sugar",
            "Aids weight management", "Enhances bone strength", "Reduces inflammation",
            "Improves skin health", "Supports brain function", "Balances cholesterol",
            "Enhances energy", "Supports liver function", "Aids detoxification",
        ]

        # ---------- 1) HerbOrFood (>= target) ----------
        herborfood_records = []
        pk_counter = 1

        base_herbs = [(name, "herb") for name in herb_names]
        base_foods = [(name, "food") for name in food_names]
        base_extras = [(name, "food") for name in extra_pool]

        base_items = base_herbs + base_foods + base_extras

        target_foods = int(options["foods"]) if options.get("foods") is not None else 650

        # Expand to reach >= target by adding variants
        variants = ["Fresh", "Organic", "Local", "Dried", "Roasted", "Toasted", "Sprouted"]
        while len(base_items) < target_foods:
            base = random.choice(base_herbs + base_foods)
            variant = random.choice(variants)
            name_variant = f"{base[0]} ({variant})"
            base_items.append((name_variant, base[1]))

        # Deduplicate by name just in case
        seen = set()
        unique_items = []
        for name, cat in base_items:
            if name not in seen:
                seen.add(name)
                unique_items.append((name, cat))

        # If still short, synthesize generic names
        synth_index = 1
        while len(unique_items) < target_foods:
            unique_items.append((f"Nutri Item {synth_index}", random.choice(["herb", "food"])) )
            synth_index += 1

        # Truncate to exactly target count
        unique_items = unique_items[:target_foods]

        for name, category in unique_items:
            nutrients = ", ".join(sorted(random.sample(nutrient_pool, k=random.randint(4, 7))))
            benefits = ", ".join(sorted(random.sample(benefit_phrases, k=random.randint(2, 4))))
            herborfood_records.append({
                "model": "nutrition.herborfood",
                "pk": pk_counter,
                "fields": {
                    "name": name,
                    "category": category,
                    "nutrients": nutrients,
                    "benefits": benefits,
                },
            })
            pk_counter += 1

        first_food_pk = 1
        last_food_pk = pk_counter - 1

        # ---------- 2) HealthIssue (>= target) ----------
        health_issue_names = [
            "Anemia", "Diabetes", "Immunity Weakness", "Obesity", "High Blood Pressure",
            "Heart Health", "Eye Health", "Bone Strength", "Kidney Health", "Liver Health",
            "Skin Glow", "Hair Fall", "Stress Relief", "Digestion Problems", "Acidity",
            "Thyroid Imbalance", "Arthritis", "Joint Pain", "Acne", "Allergies",
            "Asthma", "Cold & Cough", "Flu Recovery", "Low Energy", "Fatigue",
            "Constipation", "IBS", "Ulcer Care", "Acne Scars", "PCOS Support",
            "Menstrual Cramps", "Pregnancy Nutrition", "Postnatal Recovery", "Anxiety",
            "Depression Support", "Sleep Issues", "Insomnia", "Cholesterol Control",
            "Osteoporosis", "Gout", "Uric Acid Control", "Detox Support", "Hydration",
            "Cognitive Health", "Memory Support", "Vision Support", "Dental Health",
            "Respiratory Health", "Metabolism Boost", "Endurance",
        ]
        target_issues = int(options["issues"]) if options.get("issues") is not None else 60
        while len(health_issue_names) < target_issues:
            health_issue_names.append(f"Wellness Topic {len(health_issue_names)+1}")

        health_records = []
        health_pk_start = pk_counter
        for name in health_issue_names:
            desc = (
                f"{name} may impact daily well-being and performance. "
                f"This plan suggests nutrition choices traditionally considered supportive. "
                f"Consult professionals for personalized advice."
            )
            related_foods = random.sample(range(first_food_pk, last_food_pk + 1), k=random.randint(6, 12))
            health_records.append({
                "model": "nutrition.healthissue",
                "pk": pk_counter,
                "fields": {
                    "name": name,
                    "description": desc,
                    "herbs_or_foods": related_foods,
                },
            })
            pk_counter += 1

        # ---------- 3) Recipe (>= target) ----------
        recipe_titles = [
            "Dal", "Khichdi", "Upma", "Poha", "Paratha", "Stir Fry", "Salad", "Smoothie",
            "Soup", "Rasam", "Chutney", "Sandwich", "Wrap", "Bowl", "Kadhi", "Pulao",
        ]

        def pick_food_name_and_pk():
            pk = random.randint(first_food_pk, last_food_pk)
            return pk

        target_recipes = int(options["recipes"]) if options.get("recipes") is not None else 400
        recipe_records = []
        for _ in range(target_recipes):
            ingredient_pks = sorted(set(pick_food_name_and_pk() for _ in range(random.randint(3, 6))))
            # Title composed from one random ingredient index
            main_pk = random.choice(ingredient_pks)
            # Derive a pseudo name for title from main_pk by referencing fixture list index (safe bounds)
            # We can't import models here (no DB access required), use a placeholder mapping style
            # Reconstruct name from herborfood_records (list is 0-indexed; pk starts at 1)
            main_name = herborfood_records[main_pk - 1]["fields"]["name"]
            title = f"{main_name} {random.choice(recipe_titles)}"

            ingredients_text = ", ".join(
                herborfood_records[pk - 1]["fields"]["name"] for pk in ingredient_pks
            )
            steps = (
                "1) Prep ingredients. 2) Cook base until tender. "
                "3) Combine with spices and simmer. 4) Serve warm."
            )
            recipe_records.append({
                "model": "nutrition.recipe",
                "pk": pk_counter,
                "fields": {
                    "title": title,
                    "ingredients": ingredients_text,
                    "steps": steps,
                    "herbs_or_foods": ingredient_pks,
                },
            })
            pk_counter += 1

        fixture.extend(herborfood_records)
        fixture.extend(health_records)
        fixture.extend(recipe_records)

        # Sanity counts
        num_foods = len(herborfood_records)
        num_health = len(health_records)
        num_recipes = len(recipe_records)

        # Write file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(fixture, f, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Fixture written to {output_rel} (HerbOrFood={num_foods}, HealthIssue={num_health}, Recipe={num_recipes}, Total={len(fixture)})"
            )
        )


