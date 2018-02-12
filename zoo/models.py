from django.db import models

class Cage(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False)
    size = models.IntegerField(null=True,blank=False)
    def __str__(self):
        return self.name


class Type_cage(models.Model):
    name = models.CharField(max_length=30, null=True, blank=False)
    def __str__(self):
        return self.name


class Animal(models.Model):
    choices =(('Lion','lion'),('Elephant','elephant'),('Monkey','monkey'),('Flamingo','flamingo'),('Giraffe','giraffe'))
    name = models.CharField(max_length=30,null=True, blank=False)
    age = models.IntegerField(null=True)
    type = models.CharField(max_length=30,null=True, blank=False, choices=choices)

    cid = models.ForeignKey(Cage, on_delete=models.CASCADE)
    type_cage = models.ForeignKey(Type_cage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name