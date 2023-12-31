from django.db import models
from django.urls import  reverse


# Create your models here.
class category(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_name = models.SlugField(max_length =50, unique= True )
    slug= models.SlugField(max_length =100, unique= True )
    description=models.TextField(max_length =100, blank= True )
    cat_image=models.FileField(upload_to='photos/categories', blank= True )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
        


    def __str__(self) :
        return self.category_name
