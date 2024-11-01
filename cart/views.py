from django.shortcuts import render,redirect,get_object_or_404
from store.models import * 
from cart.models import *
from django.contrib.sessions.models import Session
from django.http import HttpResponse

# Create your views here.

def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

# def car_id(request):
#     cart=request.session.get('cart_id',None)
#     if not cart:
#         cart=f"cart_{request.session_key}"
#         request.session['cart_id']=cart
#     return cart


def cart_overview(request,total=0,quantity=0,cart_items=[]):
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax=(2 * total)/100
        grand_total=total+tax
    except Cart.DoesNotExist:
        cart=None
        cart_item=[]
        total=0
        quantity=0
        tax=0
        grand_total=0
        # cart=Cart.objects.create(cart_id=cart_id)

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'cart_overview.html',context)


def add_cart(request,id):
    
    product=Product.objects.get(id=id)
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))#get the cart using the cart_id present in the sesion
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=cart_id(request))
    cart.save()

    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1 
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect ('cart_overview')

def delete_cart(request,id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_overview') 
def delete_cart_item(request,id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart_overview')



def cart_update(request):
    return render 