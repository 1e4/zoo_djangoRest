from django.conf.urls import url, include
from . import views
from . views import AnimalViewSet,CageViewSet, UserViewSet
from rest_framework import renderers

Animal_list = AnimalViewSet.as_view({
    'get': 'retrieve',
     })

Animal_detail = AnimalViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy' })

Animal_highlight = AnimalViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

Cage_list = CageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy' })

Cage_detail = CageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy' })

Cage_highlight = CageViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

User_list = UserViewSet.as_view({
    'get': 'list'
})
User_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = [
    url(r'^api/animal$', Animal_list,  name='animal-list'),
    url(r'^api/animal/(?P<pk>[0-9]+)/$', Animal_detail, name='animal-detail'),

    url(r'^api/cage$', Cage_list,  name='cage-list'),
    url(r'^api/cage/(?P<pk>[0-9]+)/$', Cage_detail, name='cage-detail'),
    url(r'^users$', User_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', User_detail, name='user-detail'),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]