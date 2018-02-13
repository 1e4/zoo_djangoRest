

from .models import Animal,Cage
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    animal = serializers.PrimaryKeyRelatedField(many=True, queryset=Animal.objects.all())
    cage = serializers.PrimaryKeyRelatedField(many=True, queryset=Cage.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'animal', 'cage')


class AnimalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Animal
        fields = ('url', 'name', 'age','type', 'cid')

class CageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cage
        fields = ('url', 'name', 'size')



