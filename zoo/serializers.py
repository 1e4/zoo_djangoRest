

from .models import Animal,Cage
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    animal =  serializers.HyperlinkedRelatedField(many=True, view_name='animal-detail', read_only=True)
    cage =  serializers.HyperlinkedRelatedField(many=True, view_name='cage-detail', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'animal', 'cage')


class AnimalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Animal
        fields = ('id','url', 'name', 'age','type', 'cid', )

class CageSerializer(serializers.HyperlinkedModelSerializer):
    animals = serializers.SlugRelatedField(many=True, slug_field='name' ,read_only=True)

    class Meta:
        model = Cage
        fields = ('id','url', 'name', 'size', 'animals')



