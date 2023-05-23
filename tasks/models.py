from django.db import models

# Create your models here.
class PrivateKeys(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    private_key = models.CharField(max_length=200)
    type= models.CharField(max_length=10)


class AddressData(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100)
    type= models.CharField(max_length=10)
