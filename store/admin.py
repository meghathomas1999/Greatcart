from django.contrib import admin
# Register your models here.
from.models import product 

class productAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'create_date', 'modified_date', 'is_available' )
    prepopulated_Fields= ['slug', ('product_name',) ]

admin.site.register(product, productAdmin)