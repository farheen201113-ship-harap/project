from django.db import models

def product_image_path(instance, filename):
    return f'products/{filename}'

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    # Basic Info
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    original_price = models.IntegerField(blank=True, null=True, help_text="Original price before discount (leave blank if no discount)")
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    # Specifications
    processor = models.CharField(max_length=200, blank=True, help_text="e.g., Intel Core i7-13700H")
    ram = models.CharField(max_length=100, blank=True, help_text="e.g., 16 GB DDR5")
    storage = models.CharField(max_length=100, blank=True, help_text="e.g., 512 GB NVMe SSD")
    display = models.CharField(max_length=200, blank=True, help_text="e.g., 15.6\" FHD IPS 144Hz")
    graphics = models.CharField(max_length=200, blank=True, help_text="e.g., NVIDIA RTX 4050")
    battery = models.CharField(max_length=100, blank=True, help_text="e.g., 72 Wh, Up to 10 hrs")
    os = models.CharField(max_length=100, blank=True, verbose_name="Operating System", help_text="e.g., Windows 11 Home")
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., 1.9 kg")

    # Features (comma separated)
    features = models.TextField(blank=True, help_text="Enter features separated by commas. e.g., Backlit KB, Thunderbolt 4, WI-FI 6E, Fingerprint")

    # Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, help_text="e.g., 4.8")
    rating_count = models.IntegerField(default=0, help_text="Number of ratings")

    # Badges
    is_new = models.BooleanField(default=False, verbose_name="Show 'NEW' badge")
    is_assured = models.BooleanField(default=True, verbose_name="Show 'TechNova Assured' badge")
    in_stock = models.BooleanField(default=True, verbose_name="In Stock")
    stock_count = models.IntegerField(default=10, help_text="Number of items in stock")

    # Delivery & Offers
    free_delivery = models.BooleanField(default=True, verbose_name="Free Delivery")
    delivery_text = models.CharField(max_length=200, blank=True, default="Free delivery by Tomorrow. In Stock", help_text="e.g., Free delivery by Tomorrow. In Stock")
    emi_available = models.BooleanField(default=False, verbose_name="EMI Available")
    emi_text = models.CharField(max_length=200, blank=True, help_text="e.g., EMI from 2,533/month. No Cost EMI available")
    offer_text = models.CharField(max_length=200, blank=True, help_text="e.g., 10% off with HDFC / ICICI cards")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []

    def __str__(self):
        return self.name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.first_name} - {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    payment_method = models.CharField(max_length=50)
    total_amount = models.IntegerField()
    order_id = models.CharField(max_length=20)
    status = models.CharField(max_length=50, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.customer.first_name} - {self.product.name}"