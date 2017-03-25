from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=500)
    about = models.CharField(max_length=1000)
    slogan = models.CharField(max_length=500)    

    def __str__(self):
        return self.user.username

class Product(models.Model):
    PRODUCT_CHOICES = (
        ("EL", "Electronics"),
        ("CO", "Collectibles"),
        ("FI", "Finance"),
        ("HO", "Home"),
        ("TR", "Travel")
    )

    title = models.CharField(max_length=500)
    category = models.CharField(max_length=2, choices=PRODUCT_CHOICES)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(default=5)
    photo = models.FileField(upload_to='products')
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
