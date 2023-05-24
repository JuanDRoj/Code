from django.db import models

# Create your models here.
class PrivateSeeds(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    seed = models.CharField(max_length=200)
    seed_key=models.CharField(max_length=100)

class AddressData(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100)
    type= models.CharField(max_length=10)
