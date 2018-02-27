from django.conf.urls import url, include

from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from snippets import views
from snippets.views import SnippetViewSet, UserViewSet, api_root


## Using Routers ##

# create a router and register ViewSets
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# the API URLs are now automatically determined by the Router
urlpatterns = [
    url(r'^', include(router.urls))
]





# ## Explicitly creating a set of views from a ViewSet to see what is going on under the hood ##
# 
# snippet_list = SnippetViewSet({
#     'get': 'list',
#     'post': 'create'
# })
# 
# snippet_detail = SnippetViewSet({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# 
# snippet_highlight = SnippetViewSet({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# 
# user_list = UserViewSet({
#     'get': 'list'
# })
# 
# user_detail = UserViewSet({
#     'get': 'retrieve'
# })
# 
# 
# 
# 
# urlpatterns = format_suffix_patterns([
#     url(r'^$', api_root),
#     url(r'^snippets/$', snippet_list, name='snippet-list'),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
#     url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
#     url(r'^users/$', user_list, name='user-list'),
#     url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
#     url(r'^api-auth/', include('rest_framework.urls'))
# ])
