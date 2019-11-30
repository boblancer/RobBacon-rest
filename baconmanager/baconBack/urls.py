from django.urls import path

from .views import *

urlpatterns = [path('', index, name='index'),
               path('users/', list_user.as_view(), name="user_all"),
               path('usersTest/', user_test)]