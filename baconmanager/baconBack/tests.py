from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import User
from .serializers import UserSerializer

# Create your tests here.

class UserViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def add_user(fn="", ln="", id=""):
        if not fn and not ln and not id:
            User.objects.create(firstName=fn, lastName=ln, lineID=id)

class getUserTest(UserViewTest):

    def get_all_user(self):
        response = self.client.get()
        # fetch the data from db
        expected = User.objects.all()
        serialized = UserSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
