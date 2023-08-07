# Import the relevant model
from store.models import Product

# Query all products
all_products = Product.objects.all()
print(all_products)
