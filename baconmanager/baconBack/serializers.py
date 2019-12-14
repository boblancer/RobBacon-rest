from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("firstName", "lastName", "lineID")

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("classID", "sessionID", "userID")

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ("superUserID", "ID", "name", "description", "hwID")

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("classID", "userID")

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("ID", "topic", "description", "start", "end")