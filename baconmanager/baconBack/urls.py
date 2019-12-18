from django.urls import path

from .views import *

urlpatterns = [path('', webhook, name='index'),
               path('usersTest/<int:pk>', UserDetail.as_view(), name="UserDetailsAPI"),
               path('usersTest/', UserList.as_view(), name="UserAPI")]