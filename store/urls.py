from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name='index'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('register/',views.register_user, name='register'),
    path('password_update/',views.password_update, name='password_update'),
    path('user_update/',views.user_update, name='user_update'),
    path('info_update/',views.info_update, name='info_update'),
    path('product/<int:id>',views.product, name='product'),
    path('category_list/',views.category_list,name='category_list'),
    path('category/<str:chr>',views.category, name='category'), 
    
    path('search/',views.search,name='search'),



]
