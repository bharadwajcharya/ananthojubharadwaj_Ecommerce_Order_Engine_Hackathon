from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add-product/', views.add_product),
    path('products/', views.view_products),
    path('add-to-cart/<int:id>/', views.add_to_cart),
    path('cart/', views.view_cart),
    path('remove/<int:id>/', views.remove_from_cart),
    path('place-order/', views.place_order),
    path('orders/', views.view_orders),
    path('cancel/<int:id>/', views.cancel_order),
    path('return/<int:id>/', views.return_product),
    path('low-stock/', views.low_stock),
]