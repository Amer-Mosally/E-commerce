from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(validators = [MinValueValidator(1)])
    auction = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='auction',default='')
    winner = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.price} bid by {self.user}"

    def get_absolute_url(self):
        return reverse("index") 

class Listing(models.Model):    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    item = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255, default='')
    image = models.ImageField( null=True, blank=True, upload_to='media/')

    price = models.FloatField(validators = [MinValueValidator(1)])
    final_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='final_bid', blank=True, null=True)
    closed = models.BooleanField(default=False)
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    

    def __str__(self):
        return 'Item: ' +self.item +'  |   Owner: '+ str(self.owner)

    def get_absolute_url(self):
        return reverse("index") 
    
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('index')

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")

class Comment(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.post.item, self.title)