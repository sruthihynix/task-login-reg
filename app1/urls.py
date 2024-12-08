from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('products/', views.product, name='product'),
    path('addToCart/<int:product_id>/', views.addToCart, name='addToCart'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('remove/<int:item_id>/', views.remove, name='remove'),
]


