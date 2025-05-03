from django.core.management.base import BaseCommand
from faker import Faker
from products.models import ProductCategoryModel
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate fake categories'
    def handle(self, *args, **options):
        fake = Faker()
        # Generate fake categories
        for _ in range(10):
            title = fake.word()
            slug = slugify(title, allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(title=title, slug=slug)
        self.stdout.write(self.style.SUCCESS(
            'Successfully generated 10 fake categories'))
        