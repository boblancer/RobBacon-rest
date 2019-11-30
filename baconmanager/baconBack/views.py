from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status

from .models import User
from .serializers import UserSerializer

# Create your views here.

def index(request):
    return HttpResponse("Hello.")

@api_view(['GET', 'POST'])
def user_test(request):

    if request.method == 'GET':
        qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class list_user(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


