from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from django.utils.text import slugify
from products.models import ProductModel, ProductCategoryModel
from accounts.models import CustomeUser,UserType
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Generate fake products with color stock'

    def handle(self, *args, **options):
        fake = Faker()
        user = CustomeUser.objects.get(type=UserType.superuser.value)

        # لیست تصاویر موجود در پوشه images
        image_list = [
            "./images/1.jpg",
            "./images/2.jpg",
            "./images/3.jpg",
            "./images/4.jpg",
            "./images/5.jpg",
            "./images/6.jpg",
            "./images/7.jpg",
            "./images/8.jpg",
            "./images/9.jpg",
            "./images/10.jpg",
            "./images/11.jpg",
            "./images/12.jpg",
            "./images/13.jpg",
            "./images/14.jpg",
            "./images/15.jpg",
            "./images/16.jpg",
            "./images/17.jpg",
            "./images/18.jpg",
            
            # Add more images if necessary
        ]
        categories = list(ProductCategoryModel.objects.all())
        

        if not categories:
            self.stdout.write(self.style.WARNING('❌ No categories found. Run category seeder first.'))
            return


        for _ in range(10):  # ایجاد 10 محصول
            user=user
            title = fake.sentence(nb_words=3)
            slug = slugify(title, allow_unicode=True)
            description = fake.paragraph()
            brief_description = fake.paragraph()
            avg_rate = round(random.uniform(0, 5), 1)
            status = 1  # منتشر شده
            price = Decimal(random.randint(1000, 50000))
            discount_percent = random.randint(0, 50)
            stock = fake.random_int(min=0, max=10)

            # انتخاب تصویر تصادفی
            selected_image = random.choice(image_list)
            image_path = BASE_DIR / selected_image
            image_obj = File(open(image_path, "rb"), name=Path(selected_image).name)

            # ایجاد محصول
            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                description=description,
                brief_description=brief_description,
                avg_rate=avg_rate,
                status=status,
                price=price,
                discount_percent=discount_percent,
                stock=stock,
                image=image_obj,
            )

            # اضافه کردن دسته‌بندی تصادفی به محصول
            product.category.set(random.sample(categories, k=random.randint(1, len(categories))))

          

        self.stdout.write(self.style.SUCCESS('✅ Successfully generated 10 fake products with colors and stock'))