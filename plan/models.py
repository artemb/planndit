from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    webfleet_account = models.CharField(max_length=32, blank=True)
    webfleet_username = models.CharField(max_length=32, blank=True)
    webfleet_password = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.user.username


class Location(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='')
    postcode = models.CharField(max_length=255, default='')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.address


class Vehicle(models.Model):
    account = models.ForeignKey(Account)
    location = models.ForeignKey(Location, null=True)
    name = models.CharField(max_length=64, blank=True)
    external_id = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Route(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=32)
    account = models.ForeignKey(Account)
    vehicle = models.ForeignKey(Vehicle, null=True)
    created = models.DateField(auto_now_add=True)
    distance = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    date = models.DateField(blank=True, auto_now_add=True)
    status = models.CharField(max_length=10, default='New')


class Order(models.Model):
    location = models.ForeignKey(Location)
    order = models.IntegerField(default=0)
    route = models.ForeignKey(Route, related_name='orders')
    reference = models.CharField(max_length=32)
    commentary = models.CharField(max_length=255, blank=True)
    distance = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.location.address

    class Meta:
        ordering = ('order',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    key = models.CharField(max_length=32)
    value = models.CharField(max_length=255)


class LocationCache(models.Model):
    from_latitude = models.FloatField(null=False)
    from_longitude = models.FloatField(null=False)
    to_latitude = models.FloatField(null=False)
    to_longitude = models.FloatField(null=False)
    distance = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
