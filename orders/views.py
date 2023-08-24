from django.shortcuts import render,redirect
from carts.models import CartItem
from . forms import OrderForm
from .models import Order,Payment,OrderProduct
import datetime
import json
from decimal import Decimal
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Order
from django.http import JsonResponse


# Create your views here.
def place_order(request,total = 0,  quantity = 0,):
    current_user =request.user
    #if the cart count less than or equal to redirect store
    cart_items = CartItem.objects.filter(user =current_user)
    cart_count =cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price) * cart_item.quantity 
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax     
         
    if request.method =="POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all the billing information  inside the  order database table
            data =Order()
            data.user =current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.email=form.cleaned_data['email']
            data.phone_number=form.cleaned_data['phone_number']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax =tax
            data.ip =request.META.get('REMOTE_ADDR')
            data.save()
            #Genertae order_no
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(int(yr),mt,dt)
            current_date = d.strftime("%y%m%d")
            order_number =current_date + str(data.id)
            data.order_number =order_number
            data.save()
            order = Order.objects.get(user = current_user,is_orderd =False,order_number =order_number)
            context ={
                'order': order,
              'cart_items':cart_items,
              'total' :total,
              'tax' :tax,
              'grand_total':grand_total
            }
            return render(request,'orders/payments.html',context)
        else:
            return redirect('checkout')
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user,is_orderd =False,order_number =body['order_ID'])
    amount_paid = Decimal(str(order.order_total))
    print("Trans ID:", body['trans_ID'])
    print("Payment Method:", body['payment_method'])
    print("Amount Paid:", Order.order_total)  # Make sure this is the correct attribute
    print("Status:", body['status'])
    #store transaction details inside payment model 
    payment = Payment(
        user = request.user,
        payment_id = body['trans_ID'],
        payment_method = body['payment_method'],
        payment_paid =amount_paid,
        # amount_paid = Order.order_total,
        status =body['status'],


    )
    payment.save()
    order.payment=payment
    order.is_orderd=True
    order.save()
    car_items = CartItem.objects.filter(user = request.user)
    for Item in car_items:
        orderproduct =OrderProduct()
        orderproduct.order_id = order.id 
        orderproduct.payment=payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = Item.product_id
        orderproduct.quantity = Item.quantity
        orderproduct.product_price =Item.product.price 
        orderproduct.ordered =True
        orderproduct.save()
        # orderProduct.variations = Item.variations
        cart_item=CartItem.objects.get(id = Item.id)
        product_variations = cart_item.variations.all()
        orderproduct =OrderProduct.objects.get(id = orderproduct.id )
        orderproduct.variations.set(product_variations)
        orderproduct.save()
        product=Product.objects.get(id = Item.product_id)
        product.stock -= Item.quantity
        product.save()
    CartItem.objects.filter(user=request.user).delete()
    mail_subject = "Thank you for your order"
    message = render_to_string('orders/order_received_email.html',{
                'user':request.user,
                'order':order,
                
                

    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    data = {
        'order_number':order.order_number,
        'trans_ID'    :payment.payment_id,



    }
    return JsonResponse(data)












    return render(request,'orders/payments.html')

def order_complete(request):
    
    order_number =request.GET.get('order_number')
    trans_ID=request.GET.get('payment_id')
    try:
        print("enter in to try block")
        order =Order.objects.get(order_number=order_number,is_orderd=True)
        ordered_products =OrderProduct.objects.filter(order_id=order.id)
        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        payment =Payment.objects.get(payment_id =trans_ID)
        print("ordered_products",ordered_products)
        print("order_number",order_number)
        context ={
            'order':order,
          'ordered_products':ordered_products,
        'order_number'    :order.order_number,
        'trans_ID'        :payment.payment_id,
        'payment'          :payment,
        'sub_total'          :sub_total,
        
        }  
        print()     
        return render(request,'orders/order_complete.html',context)
    except(Payment.DoesNotExist,Order.DoesNotExist):
        print("entter in to except block")
        return redirect('home')



    
         