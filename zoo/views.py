
from .models import Animal,Cage
from .serializers import AnimalSerializer,CageSerializer, UserSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.http import HttpResponse ,JsonResponse
from django.http import Http404



@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'Animal': reverse('animal-list', request=request, format=format),
        'Cage': reverse('cage-list', request=request, format=format),})



class AnimalViewSet(viewsets.ModelViewSet):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)


    def perform_update(self, serializer):

        last_cage = self.request.POST['cid'][-2] # the cage name we want to put animal in it
        newSizeOfCage = len(Cage.objects.filter(name=last_cage)[0].animals.all()) + 1  # looking for the new size after put the animal
        size = Cage.objects.filter(name=last_cage)[0].size # the old size of the cage

        value = 0
        if newSizeOfCage <= size: # if there is a empty space

            if self.request.POST['type'] == 'Lion':# if the animal is lion
                x = 'Flamingo'
            if self.request.POST['type'] == 'Flamingo':
                x = 'Lion'
            else:  # for other animals, just save it
                serializer.save(owner=self.request.user)

            for ty in Cage.objects.filter(name=last_cage)[0].animals.all():  # look for is there any flamingo in the cage

                if ty.type == x :
                    value += 1
            if value == 0:  # there is no flamingo or lion
                import pdb;
                pdb.set_trace()
                serializer.save(owner=self.request.user)  # save it
            else:  # so there is flamingo
                import pdb;
                pdb.set_trace()
                raise Http404("Pick another cage.")



        else:  # if there is no emty space
            raise Http404("The cage is full. Pick an another cage")



    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, pk, *args, **kwargs ):
        Animal = self.get_object()

        return Response(Animal.highlighted)

    '''' YOU CAN'T PUT LIONS AND FLAMINGOS IN THE SAME CAGE! '''
    def perform_create(self,  serializer):
        cage = self.request.POST['cid'][-2]
        newSizeOfCage = len(Cage.objects.filter(name=cage)[0].animals.all()) + 1 # looking for the new size after put the animal
        size = Cage.objects.filter(name=cage)[0].size # the old size of the cage
        value = 0
        if newSizeOfCage <= size: # if there is a empty space
            if self.request.POST['type'] == 'Lion': # if the animal is lion
                for ty in Cage.objects.filter(name=cage)[0].animals.all():  # look for is there any flamingo in the cage
                    if ty.type == 'Flamingo':
                        value += 1
                if value==0: # there is no flamingo
                    import pdb;pdb.set_trace()
                    serializer.save(owner=self.request.user) # save it
                else: # so there is flamingo
                    raise Http404("There is flamingo in the cage. Pick another cage.")

            if self.request.POST['type'] == 'Flamingo': # if the animal is flamingo
                for type in Cage.objects.filter(name=cage)[0].animals.all():  # look for is there any lion in the cage
                    if type == 'Lion':
                        value += 1
                if value == 0:  # there is no lion
                    serializer.save(owner=self.request.user)  # save it
                else: # so there is lion
                    raise Http404("There is lion in the cage. Pick another cage.")
            else: # for other animals, just save it
                serializer.save(owner=self.request.user)

        else: # if there is no emty space
            raise Http404("The cage is full. Pick an another cage")





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
