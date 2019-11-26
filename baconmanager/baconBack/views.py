from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# Create your views here.

def index(request):
    return HttpResponse("Hello.")

class list_user(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


