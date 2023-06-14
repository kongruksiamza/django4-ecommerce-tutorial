from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cartapp.models import Cart,CartItem
from orderapp.models import Order,OrderDetail
from productsapp.models import Product
from cartapp.views import create_cartId

@login_required(login_url="/login")
def orderHistory(request):
    orders=Order.objects.filter(customer=request.user)
    return render(request,"orderHistory.html",{"orders":orders})

@login_required(login_url="/login")
def orderDetail(request,order_id):
    order=Order.objects.get(pk=order_id)
    if order.customer==request.user:
        order_items=OrderDetail.objects.filter(order=order)
        return render(request,"orderDetail.html",{"order":order,"order_items":order_items})
    else:
        return redirect("/orderHistory")
    

# Create your views here.
@login_required(login_url="/login")
def order(request):
    if request.method=="POST":
        fullname=request.POST["fullname"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
        cartItem=CartItem.objects.filter(cart=cart)
        total=0
        for item in cartItem:
            total+=(item.product.price * item.quantity)
        #สร้างใบสั่งซื้อสินค้า    
        order=Order.objects.create(
            fullname=fullname,
            phone=phone,
            address=address,
            total=total,
            customer=request.user
        )
        order.save()
        #บันทึกรายการสั่งซื้อและตัด Stock
        for item in cartItem:
            order_detail=OrderDetail.objects.create(
                product=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                order=order
            )
            order_detail.save()
            #ตัด Stock 
            product=Product.objects.get(pk=item.product.id)
            product.stock=int(item.product.stock-order_detail.quantity)
            product.save()
            item.delete()
        cart.delete()
        return render(request,"ordercomplete.html")
    else:
        return render(request,"order.html")