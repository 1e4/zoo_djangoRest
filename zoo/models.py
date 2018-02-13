
from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

choices =(('Lion','lion'),('Elephant','elephant'),('Monkey','monkey'),('Flamingo','flamingo'),('Giraffe','giraffe'))

class Cage(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False, unique=True)
    size = models.IntegerField(null=True,blank=False)
    highlighted = models.TextField(null=True)

    def __str__(self):
        return self.name

class Animal(models.Model):

    name = models.CharField(max_length=30,null=True, blank=False, unique=True)
    age = models.IntegerField(null=True)
    type = models.CharField(max_length=30,null=True, blank=False, choices=choices )
    cid = models.ForeignKey(Cage, related_name='animals' ,on_delete=models.CASCADE , null=False)
    highlighted = models.TextField(null=True)

    def __str__(self):
        return self.name

def save(self, *args, **kwargs):

    lexer = get_lexer_by_name(self.language)
    linenos = self.linenos and 'table' or False
    options = self.title and {'title': self.title} or {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super(Animal, self).save(*args, **kwargs)
    super(Cage, self).save(*args, **kwargs)