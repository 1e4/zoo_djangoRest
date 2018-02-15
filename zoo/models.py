
from django.db import models

choices = (('Lion','lion'),('Elephant','elephant'),('Monkey','monkey'),('Flamingo','flamingo'),('Giraffe','giraffe'))

class Cage(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False, unique=True)
    size = models.IntegerField(null=True,blank=False)

    owner = models.ForeignKey('auth.User', related_name='Cage', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Animal(models.Model):

    name = models.CharField(max_length=30,null=True, blank=False, unique=True)
    age = models.IntegerField(null=True)
    type = models.CharField(max_length=30,null=True, blank=False, choices=choices )
    cid = models.ForeignKey(Cage, related_name='animals' ,on_delete=models.CASCADE , null=False)

    owner = models.ForeignKey('auth.User', related_name='Animal', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
