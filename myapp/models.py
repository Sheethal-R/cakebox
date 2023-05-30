from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Cakebox(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    flavour=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    shape=models.CharField(max_length=200)
    weight=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    layer=models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name
