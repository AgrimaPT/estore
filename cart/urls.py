from django.urls import path
from .import views

urlpatterns = [
    path('',views.cart_overview,name='cart_overview'),
    path('add_cart/<int:id>',views.add_cart,name='add_cart'),
    path('delete_cart/<int:id>',views.delete_cart,name='delete_cart'),
    path('delete_cart_item/<int:id>',views.delete_cart_item,name='delete_cart_item'),
    path('update/',views.cart_update,name='cart_update'),
    

]
