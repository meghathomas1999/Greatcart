from django.db import models
from store. models  import Product,Variation
from accounts.models import Account
# # Create your models here.
class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart_id =  models.CharField(max_length= 250, blank=True)
    date_added = models. DateField(auto_now_add=True)

    def __str__(self) :
        return  self. cart_id

class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=50,default='seleced_color')
    size = models.CharField(max_length=50,default='seleced_size')
    def __str__(self) :
        return f"{self.product}-{self.color}-{self.size}"
    def sub_total(self):
        return self.product.price * self.quantity

    def total_price(self):
        return self.product.price * self.quantity

    




    

    