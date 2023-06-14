from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from productsapp.models import Product
from cartapp.models import Cart,CartItem

def create_cartId(request):
    cart = request.session.session_key
    if not cart :
        cart=request.session.create()
    return cart

@login_required(login_url="/login")
def removeCart(request,product_id):
    cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
    product=Product.objects.get(pk=product_id)
    cartItem=CartItem.objects.get(product=product,cart=cart)#สินค้าที่ต้องการลบ
    cartItem.delete()
    return redirect("/cart")

# Create your views here.
@login_required(login_url="/login")
def cart(request):
    counter=0
    total=0
    try:
        #ดึงข้อมูลตะกร้าสินค้า
        cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
        #ดึงข้อมูลสินค้าในตะกร้า
        cartItem=CartItem.objects.filter(cart=cart)
        for item in cartItem:
            counter+=item.quantity # 3, 1
            total+=(item.product.price * item.quantity) # 3x50 , 1x100
    except (Cart.DoesNotExist,CartItem.DoesNotExist): 
        cart=None 
        cartItem=None
    return render(request,"cart.html",{"cartItem":cartItem,"total":total,"counter":counter})

@login_required(login_url="/login")
def addCart(request,product_id):
    product=Product.objects.get(pk=product_id)
    #สร้างตะกร้าสินค้า
    try:
        #มีตะกร้าสินค้า
        cart=Cart.objects.get(cart_id=create_cartId(request))
    except Cart.DoesNotExist:
        #ไม่มีตะกร้า
        cart=Cart.objects.create(
            cart_id=create_cartId(request),
            customer=request.user
        )
        cart.save()
    #บันทึกรายการสินค้าในตะกร้า
    try:
        #ซื้อสินค้าตัวเดิม
        cartitem=CartItem.objects.get(product=product,cart=cart)
        if cartitem.quantity<cartitem.product.stock:
            cartitem.quantity+=1
            cartitem.save()
    except CartItem.DoesNotExist:
        #ซื้อสินค้า
        cartitem=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cartitem.save()
    return redirect("/cart")