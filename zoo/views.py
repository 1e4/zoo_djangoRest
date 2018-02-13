
from .models import Animal,Cage
from django.db.models import F, Q
from .serializers import AnimalSerializer,CageSerializer, UserSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def api_root(request,format=None): #:8000/ de cikan linkleri tanimladik
    return Response({
        'Animal': reverse('animal-list', request=request, format=format),
        'Cage': reverse('cage-list', request=request, format=format),

    })





class AnimalViewSet(viewsets.ModelViewSet):

    queryset = Animal.objects.all()

    serializer_class = AnimalSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)



    def perform_update(self, serializer):


        x = self.get_object()# animal model
        firs_cage = self.get_object().cid.pk

        serializer.save()

        last_cage = self.get_object().cid.pk

        newSizeOfGace =  len( Cage.objects.filter(name=self.get_object().cid.pk)[0].animals.all())

        size = Cage.objects.filter(name=self.get_object().cid.pk)[0].size

        if newSizeOfGace <= size:
            Cage.objects.filter(name=firs_cage)[0].size-=1
        else:
            x.cid.pk = firs_cage

            return HttpResponse('The cage is full')

        import pdb;
        pdb.set_trace()

        serializer.save()



    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, pk, *args, **kwargs ):
        Animal = self.get_object()

        return Response(Animal.highlighted)

    def perform_create(self,  serializer):
        queryset = Animal.objects.filter()
        import pdb;pdb.set_trace()
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
