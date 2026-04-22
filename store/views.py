from django.shortcuts import render, redirect
from .models import Customer, Product, Cart, Order, Wishlist
import hashlib
import random

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def home(request):
    # Get cart and wishlist counts for logged-in users
    cart_count = 0
    wishlist_count = 0
    if 'customer_id' in request.session:
        customer = Customer.objects.get(id=request.session['customer_id'])
        cart_count = Cart.objects.filter(customer=customer).count()
        wishlist_count = Wishlist.objects.filter(customer=customer).count()
    return render(request, 'index.html', {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    })


def products_page(request):
    laptops = Product.objects.filter(category='Laptop')
    headphones = Product.objects.filter(category='Headphones')
    mobile_phones = Product.objects.filter(category='Mobile Phone')
    watches = Product.objects.filter(category='Smart Watch')

    # Get wishlist and cart product IDs for logged-in users
    wishlist_product_ids = []
    cart_product_ids = []
    cart_count = 0
    wishlist_count = 0

    if 'customer_id' in request.session:
        customer = Customer.objects.get(id=request.session['customer_id'])
        wishlist_product_ids = [str(id) for id in Wishlist.objects.filter(
            customer=customer
        ).values_list('product_id', flat=True)]
        cart_product_ids = [str(id) for id in Cart.objects.filter(
            customer=customer
        ).values_list('product_id', flat=True)]
        cart_count = Cart.objects.filter(customer=customer).count()
        wishlist_count = Wishlist.objects.filter(customer=customer).count()

    return render(request, 'products.html', {
        'laptops': laptops,
        'headphones': headphones,
        'mobile_phones': mobile_phones,
        'watches': watches,
        'wishlist_product_ids': wishlist_product_ids,
        'cart_product_ids': cart_product_ids,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'MEDIA_URL': '/media/',
    })

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed = hash_password(password)
        try:
            customer = Customer.objects.get(email=email, password=hashed)
            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.first_name
            request.session['customer_email'] = customer.email
            # Ensure session is saved
            request.session.modified = True
            request.session.save()
            return redirect('/')
        except Customer.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid email or password!'
            })
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})
        if len(password1) < 8:
            return render(request, 'register.html', {'error': 'Password must be at least 8 characters!'})
        if Customer.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered!'})
        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=hash_password(password1)
        )
        return render(request, 'login.html', {'success': 'Account created! Please login.'})
    return render(request, 'register.html')


def logout_page(request):
    request.session.flush()
    return redirect('/')


def add_to_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('/login')
    customer = Customer.objects.get(id=request.session['customer_id'])
    product = Product.objects.get(id=product_id)
    
    # Toggle cart item
    cart_item = Cart.objects.filter(customer=customer, product=product).first()
    if cart_item:
        cart_item.delete()
    else:
        Cart.objects.create(customer=customer, product=product)

    # Check if coming from wishlist page - move item to cart
    referer = request.META.get('HTTP_REFERER', '')
    if '/wishlist' in referer:
        Wishlist.objects.filter(customer=customer, product=product).delete()
        return redirect('/cart')

    return redirect(request.META.get('HTTP_REFERER', '/products'))


def cart_page(request):
    if 'customer_id' not in request.session:
        return redirect('/login')
    customer = Customer.objects.get(id=request.session['customer_id'])
    cart_items = Cart.objects.filter(customer=customer)
    total = sum(item.total_price() for item in cart_items)
    wishlist_count = Wishlist.objects.filter(customer=customer).count()
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_items.count(),
        'wishlist_count': wishlist_count,
    })

def remove_from_cart(request, cart_id):
    Cart.objects.filter(id=cart_id).delete()
    return redirect('/cart')

def about_page(request):
    # Get cart and wishlist counts for logged-in users
    cart_count = 0
    wishlist_count = 0
    if 'customer_id' in request.session:
        customer = Customer.objects.get(id=request.session['customer_id'])
        cart_count = Cart.objects.filter(customer=customer).count()
        wishlist_count = Wishlist.objects.filter(customer=customer).count()
    return render(request, 'about.html', {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    })


def checkout_page(request):
    if 'customer_id' not in request.session:
        return redirect('/login')
    customer = Customer.objects.get(id=request.session['customer_id'])
    cart_items = Cart.objects.filter(customer=customer)
    total = sum(item.total_price() for item in cart_items)
    wishlist_count = Wishlist.objects.filter(customer=customer).count()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment_method = request.POST.get('payment')
        order_id = 'TN' + str(random.randint(100000, 999999))

        Order.objects.create(
            customer=customer,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            payment_method=payment_method,
            total_amount=total,
            order_id=order_id,
            status='Confirmed'
        )

        cart_items.delete()
        return render(request, 'checkout.html', {
            'success': True,
            'order_id': order_id,
            'total': total,
            'cart_count': 0,
            'wishlist_count': wishlist_count,
        })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_items.count(),
        'wishlist_count': wishlist_count,
    })


# ═══════════════════════════ MY ORDERS ═══════════════════════════
def orders_page(request):
    if 'customer_id' not in request.session:
        return redirect('/login')
    customer = Customer.objects.get(id=request.session['customer_id'])
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    cart_count = Cart.objects.filter(customer=customer).count()
    wishlist_count = Wishlist.objects.filter(customer=customer).count()
    return render(request, 'orders.html', {
        'orders': orders,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    })


# ═══════════════════════════ WISHLIST ═══════════════════════════
def wishlist_page(request):
    if 'customer_id' not in request.session:
        return redirect('/login')
    customer = Customer.objects.get(id=request.session['customer_id'])
    wishlist_items = Wishlist.objects.filter(customer=customer).order_by('-added_at')
    cart_count = Cart.objects.filter(customer=customer).count()
    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items,
        'cart_count': cart_count,
        'wishlist_count': wishlist_items.count(),
    })


def add_to_wishlist(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('/login')
    customer = Customer.objects.get(id=request.session['customer_id'])
    product = Product.objects.get(id=product_id)
    wishlist_item = Wishlist.objects.filter(customer=customer, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(customer=customer, product=product)
    return redirect(request.META.get('HTTP_REFERER', '/products'))


def remove_from_wishlist(request, wishlist_id):
    if 'customer_id' not in request.session:
        return redirect('/login')
    Wishlist.objects.filter(id=wishlist_id).delete()
    return redirect('/wishlist')


def update_cart_quantity(request, cart_id):
    if 'customer_id' not in request.session:
        return redirect('/login')
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = Cart.objects.get(id=cart_id, customer_id=request.session['customer_id'])
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        cart_item.save()
    return redirect('/cart')
