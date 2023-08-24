from django.shortcuts import render, redirect
from store.models import Product
from . models import  CartItem, Cart
from django.http import  HttpResponse
from django.shortcuts import get_object_or_404
from store.models import Variation
from django.contrib.auth.decorators import login_required

def Carts_id(request,product=None,selected_color = None, selected_size = None):
    cart_id= request.session.session_key
    print("cart id:", cart_id)
    if not cart_id:
        request.session.save()
        cart_id = request.session.create()
        # print("Cart ID:", cart)
    if product and selected_color and selected_size:
       try:
           cart_item = CartItem.objects.get(cart__cart_id=cart_id, product=product,size = selected_size,color = selected_color)
           print("cart_item",cart_item)
           print("product",product)
           return cart_item.id if cart_item else None
       except CartItem.DoesNotExist:
            return None
    return cart_id
#his is my add cart function original code starting 
def add_Carts(request,product_id):
    product = Product.objects.get(id = product_id)
    product_variation = []
    if request.method == "POST":
        for item in request.POST:
            print("item:",item)
            key = item 
            value =request.POST.get(item)
            print("value:",value )

            try:
               variation = Variation.objects.get(product=product, variation_category__iexact = key,variation_value__iexact = value)
               print("variation:", variation)
               product_variation.append(variation)
               print("product variation",product_variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id = Carts_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = Carts_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        print("Variations in cart_item:", cart_item.variations.all())
        if len(product_variation)>0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity =1,
            cart = cart
        )
        if len(product_variation)>0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()
    from django.db import connection
    print("SQL Query:", str(connection.queries[-1]))
    return redirect("Carts")


    
    
    

    

   
                   
                   

                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                        




















def remove_Carts(request, product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    try:
       if request.user. is_authenticated:
           cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
       else:
           cart= Cart.objects.get(cart_id= Carts_id(request)) 
           cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
       if cart_item and cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
       else:
          cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('Carts')
def remove_Cart_item(request,product_id,cart_item_id):
    product = get_object_or_404(Product,id =product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = Carts_id(request))
        cart_item = CartItem.objects.get(product = product, cart=cart,id=cart_item_id)
    cart_item.delete()  
    return redirect('Carts')


def Carts(request, total = 0,  quantity = 0, cart_items = None):  
    try:
        tax= 0
        grand_total= 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active= True)
        else:
            cart = Cart.objects.get(cart_id= Carts_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active= True)
        for cart_item in cart_items:
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
@login_required(login_url='login')
def checkout(request, total = 0,  quantity = 0,cart_items = None):
    tax= 0
    grand_total= 0 
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active= True)
        else:
            cart = Cart.objects.get(cart_id= Carts_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active= True)
        for cart_item in cart_items:
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
    return render(request,'store/checkout.html',context)


