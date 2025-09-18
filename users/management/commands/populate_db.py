import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from faker import Faker

class Command(BaseCommand):
    help = 'Populates the database with fake data for development and testing.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        fake = Faker()

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create Users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(10):
            username = fake.user_name()
            password = 'password123'
            user = User.objects.create_user(username=username, password=password, email=fake.email())
            users.append(user)

        # Create Categories
        self.stdout.write('Creating categories...')
        categories = []
        category_names = ['Electronics', 'Books', 'Clothing', 'Home Goods', 'Toys']
        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name, slug=fake.slug(name))
            categories.append(category)

        # Create Products
        self.stdout.write('Creating products...')
        for _ in range(50):
            category = random.choice(categories)

            # Generate category-specific product names
            if category.name == 'Electronics':
                name = f"{fake.company()} {random.choice(['Smartphone', 'Laptop', 'Tablet', 'TV', 'Speaker'])}"
            elif category.name == 'Books':
                name = f"{fake.sentence(nb_words=3).replace('.', '')}"
            elif category.name == 'Clothing':
                name = f"{fake.color_name()} {random.choice(['Shirt', 'Dress', 'Pants', 'Jacket', 'Shoes'])}"
            elif category.name == 'Home Goods':
                name = f"{fake.word().title()} {random.choice(['Chair', 'Table', 'Lamp', 'Cushion', 'Vase'])}"
            else:  # Toys
                name = f"{fake.word().title()} {random.choice(['Toy', 'Game', 'Puzzle', 'Doll', 'Car'])}"
            
            Product.objects.create(
                category=category,
                name=name,
                description=fake.text(),
                price=round(random.uniform(10.0, 500.0), 2),
                stock=random.randint(1, 100)
            )

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
