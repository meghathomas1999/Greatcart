from django.shortcuts import render, redirect
from store.models import Product
from . models import  CartItem, Cart
from django.http import  HttpResponse
from django.shortcuts import get_object_or_404
from store.models import Variation
def Carts_id(request,product=None,selected_color = None, selected_size = None):
    cart= request.session.session_key
    print("cart id:", cart)
    if not cart:
        request.session.save()
        cart = request.session.create()
        print("Cart ID:", cart)
    if product and selected_color and selected_size:
       try:
           cart_item = CartItem.objects.get(cart__cart_id=cart, product=product,size = selected_size,color = selected_color)
           return cart_item.id if cart_item else None
       except CartItem.DoesNotExist:
            return None
    return cart

# def add_Carts(request, product_id):
#     product = Product.objects.get( id = product_id)
#     print("Product", product)
#     print("Product ID:", product_id) 
#     product_variation = []
#     if request.method == 'POST':
#         for item in request.POST:
#            key = item
#            value = request.POST[key]
#            print(f"key:{key},value:{value}")
           
#            try:
#                variation = Variation.objects.get(product=product, variation_category__iexact = key,variation_value__iexact = value)
#                product_variation.append(variation)
#            except :
#                pass
#     try:
#         cart = Cart.objects.get(cart_id= Carts_id(request))
#         print(Cart)
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(cart_id = Carts_id(request)  )
#         cart.save()
#         # existing_cart_item = CartItem.objects.filter(cart=cart,product=product, variations__in=product_variation).first()
#         # if existing_cart_item:
#         #     existing_cart_item.quantity += 1
#         #     existing_cart_item.save()
#         # else:
#         #     cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#         #     cart_item.variations.set(product_variation)
#     # return redirect('Carts')
#     try:
#         cart_item = CartItem.objects.create(product = product,quantity = 1, cart = cart)
#         if len(product_variation) >0 :
#             cart_item.variations.clear()
#             for Item in product_variation:
#                 cart_item.variations.add(Item)

#         cart_item.quantity += 1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(
#             Product = Product,
#             quantity  = 1,
#             cart = cart,


#         )
#     # cart_item.save()
#     # print(cart_item)
#     # return redirect('Carts')

#         if len(product_variation) >0 :
#             cart_item.variations.clear()
#             for Item in product_variation:
#                 cart_item.variation.add(Item)
#         cart_item.save()
#         print(cart_item)
#     return redirect('Carts')
# def add_Carts(request, product_id):
#     product = Product.objects.get(id=product_id)
#     product_variation = []

#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]
#             print(f"key:{key},value:{value}")
#             try:
#                 variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                 product_variation.append(variation)
#             except Variation.DoesNotExist:
#                 pass

#     try:
#         cart = Cart.objects.get(cart_id=Carts_id(request))
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(cart_id=Carts_id(request))

#     existing_cart_item = CartItem.objects.filter(cart=cart, product=product, variations__in=product_variation).first()

#     if existing_cart_item:
#         existing_cart_item.quantity += 1
#         existing_cart_item.save()
#     else:
#         cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#         cart_item.variations.set(product_variation)

#     return redirect('Carts')
def add_Carts(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = {}  # Use a dictionary to store variations for each product

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            print(f"key:{key},value:{value}")
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation[product_id] = product_variation.get(product_id, [])
                product_variation[product_id].append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=Carts_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=Carts_id(request))

    existing_cart_item = CartItem.objects.filter(cart=cart, product=product, variations__in=product_variation.get(product_id, [])).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.variations.set(product_variation.get(product_id, []))

    return redirect('Carts')










def remove_Carts(request, product_id,cart_item_id):
    cart= Cart.objects.get(cart_id= Carts_id(request))
    product = get_object_or_404(Product,id=product_id)
    try:
       cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
       if cart_item and cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
       else:
          cart_item.delete()
    except:
        pass
    return redirect('Carts')
def remove_Cart_item(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = Carts_id(request))
    product = get_object_or_404(Product,id =product_id)
    cart_item = CartItem.objects.filter(product = product, cart=cart,id=cart_item_id)
    print("cart_item_id:",cart_item_id)
    cart_item.delete()
    return redirect('Carts')




    
   

def Carts(request, total = 0,  quantity = 0,cart_items = None):
    tax= 0
    grand_total= 0 

    try:
        cart = Cart.objects.get(cart_id= Carts_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active= True)
        print("cart items:", cart_items)
        for cart_item in cart_items:
            print("product Name:", cart_item.product.product_name)
            print("product image url:",cart_item.product.image.url)
            total += (cart_item.product.price) * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        
    except Cart.DoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax'       : tax,
        'grand_total':grand_total,

    }


    return render(request, 'store/cart.html', context)




