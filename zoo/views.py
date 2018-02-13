
from .models import Animal,Cage
from .serializers import AnimalSerializer,CageSerializer, UserSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request,format=None): #:8000/ de cikan linkleri tanimladik
    return Response({
        'Animal': reverse('animal-list', request=request, format=format),
        'Cage': reverse('cage-list', request=request, format=format),

    })


class AnimalViewSet(viewsets.ModelViewSet):
    """ `list`, `create`, `retrieve`,
       `update` and `destroy` actions  """

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)


    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        Animal = self.get_object()
        return Response(Animal.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CageViewSet(viewsets.ModelViewSet):

    queryset = Cage.objects.all()
    serializer_class = CageSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        Cage = self.get_object()
        return Response(Cage.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
