from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.title

class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

class Sale(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Sale of {self.car} to {self.buyer.username} for ${self.sale_price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"
