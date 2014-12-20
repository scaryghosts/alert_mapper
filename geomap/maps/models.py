from django.db import models

class Alert(models.Model):
    node = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    text = models.TextField(max_length=500)
    

class Coordinates(models.Model):
    location = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)

class Cores(models.Model):
    location = models.CharField(max_length=255)
    dnsname = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

class ActiveAlerts(models.Model):
    node = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)    
