from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


from django.utils import timezone

class UserPredictModel(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    label = models.CharField(max_length=100)  # This will store the prediction result
    timestamp = models.DateTimeField(default=timezone.now)  # New field for date and time

    def __str__(self):
        return f"Prediction: {self.label}"

    
from django.utils import timezone

class yield_db(models.Model):
    crop = models.CharField(max_length=100)
    season = models.CharField(max_length=100)
    area = models.FloatField()
    area_units = models.CharField(max_length=50)
    production = models.FloatField()
    production_units = models.CharField(max_length=50)
    yield_value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)  # Date & Time field

    def __str__(self):
        return f"{self.crop} - {self.season}"





from django.contrib.auth.models import User
from django.db import models

# Customer Profile
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

# Product model for users to upload and customers to buy
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name

# Orders placed by customers
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} ordered {self.product.name}"


from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username



class Purchase(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} bought {self.product.name}"
    



from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='customer_profiles/', default='default.jpg')

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"
