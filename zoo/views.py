
from .models import Animal,Cage
from .serializers import AnimalSerializer,CageSerializer, UserSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import permissions, renderers, viewsets
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.http import Http404

@api_view(['GET'])
def api_root(request,format=None):
    return Response({
        'Animal': reverse('animal-list', request=request, format=format),
        'Cage': reverse('cage-list', request=request, format=format),})



class AnimalViewSet(viewsets.ModelViewSet):
    """ YOU CAN'T PUT LIONS AND FLAMINGOS IN THE SAME CAGE! """

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,)

    def perform_update(self, serializer):
        if serializer.data['name'] == self.request.POST['name'] and serializer.data['age'] == self.request.POST['age'] \
                and serializer.data['type'] == self.request.POST['type']:  # if name,age,type is the same for the animal
            last_cage = self.request.POST['cid'].replace("/","").replace("http:127.0.0.1:8000apicage","")  # the cage id we want to put animal in it
            c = Cage.objects.filter(id=last_cage)[0].animals.all()
            if c:  # if there are other animals in the cage
                newSizeOfCage = len(c) + 1  # looking for the new size
                size = Cage.objects.filter(id=last_cage)[0].size # the old size of the cage

                value = 0
                if newSizeOfCage <= size: # if there is a empty space
                    if self.request.POST['type'] == 'Lion':  # if the animal is lion
                        for ty in Cage.objects.filter(name=last_cage)[0].animals.all():  # look for is there any flamingo in the cage
                            if ty.type == 'Flamingo':
                                value += 1
                        if value == 0:  # there is no flamingo
                            serializer.save(owner=self.request.user)  # save it
                        else:  # so there is flamingo
                            raise Http404("There is flamingo in the cage. Pick another cage.")

                    if self.request.POST['type'] == 'Flamingo':  # if the animal is flamingo
                        for ty in Cage.objects.filter(name=last_cage)[0].animals.all():  # look for is there any lion in the cage
                            if ty.type == 'Lion':
                                value += 1
                        if value == 0:  # there is no lion
                            serializer.save(owner=self.request.user)  # save it
                        else:  # so there is lion
                            raise Http404("There is lion in the cage. Pick another cage.")
                    else:  # for other animals, just save it
                        serializer.save(owner=self.request.user)

                else:  # if there is no emty space
                    raise Http404("The cage is full. Pick an another cage")
            elif Cage.objects.filter(id=last_cage)[0].size >= 1:  # there is no other animal and there is space for an animal
                serializer.save(owner=self.request.user)
            else:
                raise Http404("Pick another cage.")

        else: #age,name or type is not the same
            raise Http404('Age, name or type is not the same for the animal')



    def perform_create(self,  serializer):

        cage = self.request.POST['cid'].replace("/","").replace("http:127.0.0.1:8000apicage","") #cage's id

        import pdb; pdb.set_trace()
        c = Cage.objects.filter(id=cage)[0].animals.all()
        if c:  # if there are other animals in the cage
            newSizeOfCage = len(c) + 1 # looking for the new size of the cage
            size = Cage.objects.filter(id=cage)[0].size # the old size of the cage
            value = 0
            if newSizeOfCage <= size: # if there is a empty space
                if self.request.POST['type'] == 'Lion': # if the animal is lion
                        for ty in c:  # look for is there any flamingo in the cage
                            if ty.type == 'Flamingo':
                                value += 1
                        if value==0: # there is no flamingo
                            serializer.save(owner=self.request.user) # save it
                        else: # so there is flamingo
                            raise Http404("There is flamingo in the cage. Pick another cage.")

                if self.request.POST['type'] == 'Flamingo': # if the animal is flamingo
                    for ty in c:  # look for is there any lion in the cage
                        if ty.type == 'Lion':
                            value += 1
                    if value == 0:  # there is no lion
                        serializer.save(owner=self.request.user)  # save it
                    else: # so there is lion
                        raise Http404("There is lion in the cage. Pick another cage.")

                else: # for other animals, just save it
                    serializer.save(owner=self.request.user)

            else: # if there is no emty space
                raise Http404("The cage is full. Pick an another cage")
        elif Cage.objects.filter(id=cage)[0].size>=1: # there is no other animal and there is space for an animal
            serializer.save(owner=self.request.user)
        else:
            raise Http404("Pick another cage.")

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, pk, *args, **kwargs ):
        Animal = self.get_object()

        return Response(Animal.highlighted)

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
