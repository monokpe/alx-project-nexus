import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from products.models import Category, Product

class Command(BaseCommand):
    """
    Custom Django management command to seed the database with initial data.

    This command can either clear and populate the database or append new products
    to existing categories.

    Usage:
    - To clear and seed (default behavior):
      python manage.py seed_db
      python manage.py seed_db --number 50  # To create 50 products in total

    - To append products to existing categories:
      python manage.py seed_db --append --products_per_category 20
    """
    help = 'Seeds the database with categories and products.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            help='The total number of products to create (used when not appending).',
            default=25
        )
        parser.add_argument(
            '--append',
            action='store_true',
            help='Append new products to existing categories without clearing the database.'
        )
        parser.add_argument(
            '--products_per_category',
            type=int,
            help='The number of products to create for each category (used with --append).',
            default=10
        )

    def handle(self, *args, **options):
        append = options['append']
        fake = Faker()

        if append:
            products_per_category = options['products_per_category']
            self.stdout.write(self.style.WARNING('Appending products to existing categories...'))
            categories = list(Category.objects.all())
            if not categories:
                self.stdout.write(self.style.ERROR('No categories found. Please create some categories first or run without --append.'))
                return

            self.stdout.write(f'Creating {products_per_category} products for each category...')
            products_to_create = []
            for category in categories:
                self.stdout.write(f'  - Creating products for category: {category.name}')
                for _ in range(products_per_category):
                    product_name = fake.company() + ' ' + fake.bs()
                    product = Product(
                        name=product_name,
                        category=category,
                        description=fake.text(max_nb_chars=500),
                        price=round(random.uniform(9.99, 999.99), 2),
                        stock=random.randint(0, 150)
                    )
                    products_to_create.append(product)
            
            Product.objects.bulk_create(products_to_create)
            total_products = len(categories) * products_per_category
            self.stdout.write(self.style.SUCCESS(f'Successfully created {total_products} products.'))

        else:  # not append
            number_of_products = options['number']
            self.stdout.write(self.style.WARNING('Clearing existing database entries...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Database cleared.'))

            self.stdout.write('Creating categories...')
            category_names = [
                'Electronics', 'Books', 'Clothing', 'Home & Garden',
                'Sports & Outdoors', 'Toys & Games', 'Health & Beauty'
            ]
            categories = []
            for cat_name in category_names:
                category, created = Category.objects.get_or_create(
                    name=cat_name,
                    defaults={'slug': slugify(cat_name)}
                )
                if created:
                    self.stdout.write(f'  - Created category: {category.name}')
                categories.append(category)
            self.stdout.write(self.style.SUCCESS('Categories created.'))

            self.stdout.write(f'Creating {number_of_products} products...')
            products_to_create = []
            for _ in range(number_of_products):
                product_name = fake.company() + ' ' + fake.bs()
                category = random.choice(categories)
                product = Product(
                    name=product_name,
                    category=category,
                    description=fake.text(max_nb_chars=500),
                    price=round(random.uniform(9.99, 999.99), 2),
                    stock=random.randint(0, 150)
                )
                products_to_create.append(product)
            
            Product.objects.bulk_create(products_to_create)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {number_of_products} products.'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))