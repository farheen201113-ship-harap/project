from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('store.urls')),
    path('products', views.products_page, name='products'),
    path('login', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('logout', views.logout_page, name='logout'),
    path('cart', views.cart_page, name='cart'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>', views.remove_from_cart, name='remove_from_cart'),
    path('about', views.about_page, name='about'),
    path('checkout', views.checkout_page, name='checkout'),
    path('orders', views.orders_page, name='orders'),
    path('wishlist', views.wishlist_page, name='wishlist'),
    path('add-to-wishlist/<int:product_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_id>', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update-cart-quantity/<int:cart_id>', views.update_cart_quantity, name='update_cart_quantity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)