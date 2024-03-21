from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    email = models.EmailField(unique=True,null=True)
    username = models.CharField(max_length=30,null=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    user = models.OneToOneField(User,related_name='customer_profile',on_delete=models.CASCADE,null=True)
    password = models.CharField(max_length=30,null=True)