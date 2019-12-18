from django.urls import path

from .views import *

urlpatterns = [path('', webhook, name='index'),
               path('usersTest/', UserList.as_view(), name="UserAPI"),
               path('usersTest/<str:pk>', UserDetail.as_view(), name="UserDetailsAPI")
              ]
