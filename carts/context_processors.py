from .models import Cart,CartItem
from . views import Carts_id
 

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart = Cart.objects.filter(cart_id=Carts_id(request)).first()
            if cart:
               cart_items = CartItem.objects.filter(cart=cart)
               for cart_item in cart_items:
                   cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0 
    return { 'cart_count' : cart_count}

