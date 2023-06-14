from django.urls import path
from orderapp import views
urlpatterns=[
    path("order",views.order),
    path("orderHistory",views.orderHistory),
    path("order/<int:order_id>",views.orderDetail,name="orderDetail")
]