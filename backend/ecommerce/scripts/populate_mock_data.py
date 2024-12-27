from faker import Faker
from ecommerce.models import Product

faker = Faker()

def populate_products():
    categories = ["Electronics", "Books", "Clothing", "Home Appliances"]
    for _ in range(100):
        Product.objects.create(
            name=faker.word(),
            category=faker.random.choice(categories),
            price=faker.random_int(min=10, max=1000),
            rating=round(faker.random.uniform(1, 5), 1),
            description=faker.text(),
            image_url=faker.image_url(),
        )
