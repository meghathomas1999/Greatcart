from django.urls import path
from  . import views

urlpatterns=[

path("", views.Carts,name="Carts"),
path('add_Carts/<int:product_id>/', views.add_Carts,name='add_Carts'),
path('remove_Carts/<int:product_id>/<int:cart_item_id>', views.remove_Carts,name='remove_Carts'),
path('remove_Cart_item/<int:product_id>/<int:cart_item_id>', views.remove_Cart_item,name='remove_Cart_item'),
path('checkout/', views.checkout,name='checkout'),
path('Carts/checkout/', views.checkout, name='checkout'),
# # urls.py
# path('add_to_cart/<int:Product_id>/', views.add_to_cart, name='add_to_cart'),
# path('remove_from_cart/<int:Product_id>/', views.remove_from_cart, name='remove_from_cart'),
# path('update_cart_quantity/<int:Product_id>/<int:Quantity>/', views.update_cart_quantity, name='update_cart_Quantity'),
#     # Add other URL patterns for other views here
]


