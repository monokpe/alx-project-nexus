
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for products and categories.'

    def handle(self, *args, **kwargs):
        if Category.objects.exists() or Product.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Aborting seed.'))
            return

        self.stdout.write("Creating categories...")
        categories = [
            "Electronics",
            "Books",
            "Home & Kitchen",
            "Apparel",
            "Sports & Outdoors"
        ]
        created_categories = []
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created category "{cat_name}"'))
            created_categories.append(category)

        self.stdout.write("Creating products...")
        products_to_create = [
            ('Laptop Pro', 'Electronics', 1200.00, 'A powerful laptop for professionals.வைக்'),
            ('Wireless Mouse', 'Electronics', 25.50, 'Ergonomic wireless mouse.'),
            ('The Great Novel', 'Books', 15.99, 'A best-selling fiction novel.'),
            ('Science of Cooking', 'Books', 22.75, 'Understand the chemistry of cooking.'),
            ('Coffee Maker', 'Home & Kitchen', 89.99, 'Brews up to 12 cups of coffee.'),
            ('Chef\'s Knife', 'Home & Kitchen', 45.00, 'High-carbon stainless steel knife.'),
            ('Running Shoes', 'Apparel', 110.20, 'Lightweight shoes for running.'),
            ('Cotton T-Shirt', 'Apparel', 9.99, '100% cotton, available in various colors.'),
            ('Yoga Mat', 'Sports & Outdoors', 30.00, 'Eco-friendly, non-slip yoga mat.'),
            ('Camping Tent', 'Sports & Outdoors', 150.00, '2-person waterproof tent.')
        ]

        for prod_name, cat_name, price, desc in products_to_create:
            category = next((c for c in created_categories if c.name == cat_name), None)
            if category:
                Product.objects.create(
                    name=prod_name,
                    category=category,
                    description=desc,
                    price=price,
                    stock=random.randint(10, 100)
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created product "{prod_name}"'))

        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))
