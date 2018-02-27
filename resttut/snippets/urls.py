from django.conf.urls import url, include

from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import SnippetViewSet, UserViewSet, api_root

## Explicitly creating a set of views from a ViewSet to see what is going on under the hood ##

snippet_list = SnippetViewSet({
    'get': 'list',
    'post': 'create'
})

snippet_detail = SnippetViewSet({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight = SnippetViewSet({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet({
    'get': 'list'
})

user_detail = UserViewSet({
    'get': 'retrieve'
})




urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
    url(r'^api-auth/', include('rest_framework.urls'))
])
