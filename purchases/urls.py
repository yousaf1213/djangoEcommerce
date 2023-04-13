from django.urls import path

from . import views

urlpatterns = [
    path('vendors/', views.vendors, name='vendors'),
    path('products/', views.products, name='products'),
    path('product/', views.prod_search, name='products'),
    path('holderlist/', views.vendorProductList, name='holder_list'),
    path('users/', views.user, name='users'),
    path('search/', views.searching, name='search'),
    path('order/', views.order, name='order'),
    path('userpurchase/', views.user_purchase_list, name='purchase_list'),
]
