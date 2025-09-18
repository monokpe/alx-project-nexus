import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from products.models import Category, Product

class Command(BaseCommand):
    """
    Custom Django management command to seed the database with initial data.
    
    This command clears existing Category and Product data and populates the database
    with a set of predefined categories and a specified number of fake products.
    This is useful for creating a consistent development and testing environment.
    
    Usage:
    python manage.py seed_db
    python manage.py seed_db --number 50  # To create 50 products
    """
    help = 'Seeds the database with categories and products.'

    def add_arguments(self, parser):
        """
        Adds command-line arguments to the command.
        
        --number: Specifies the number of products to create. Defaults to 25.
        """
        parser.add_argument(
            '--number',
            type=int,
            help='The number of products to create.',
            default=25
        )

    def handle(self, *args, **options):
        """
        The main logic for the command.
        
        This method is executed when the command is run.
        """
        number_of_products = options['number']
        fake = Faker()
        
        self.stdout.write(self.style.WARNING('Clearing existing database entries...'))
        # Clear existing data to ensure a clean slate
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database cleared.'))

        # --- Create Categories ---
        self.stdout.write('Creating categories...')
        categories = [
            'Electronics', 'Books', 'Clothing', 'Home & Garden',
            'Sports & Outdoors', 'Toys & Games', 'Health & Beauty'
        ]
        
        created_categories = []
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            if created:
                self.stdout.write(f'  - Created category: {category.name}')
            created_categories.append(category)
        
        self.stdout.write(self.style.SUCCESS('Categories created.'))

        # --- Create Products ---
        self.stdout.write(f'Creating {number_of_products} products...')
        products_to_create = []
        for _ in range(number_of_products):
            product_name = fake.company() + ' ' + fake.bs()
            category = random.choice(created_categories)
            product = Product(
                name=product_name,
                category=category,
                description=fake.text(max_nb_chars=500),
                price=round(random.uniform(9.99, 999.99), 2),
                stock=random.randint(0, 150)
            )
            products_to_create.append(product)
        
        # Use bulk_create for performance improvement
        Product.objects.bulk_create(products_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {number_of_products} products.'))
        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))

    