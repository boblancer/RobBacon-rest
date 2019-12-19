from django.db import models

# Create your models here.

class User(models.Model):
    ID = models.CharField(max_length=40, primary_key=True)
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=50)
    studentID = models.IntegerField()

    def __str__(self):
        return "ID = {} name = {} {} studentID = {}".format(self.ID, self.firstName, self.lastName, self.studentID)


class Attendance(models.Model):
    ID = models.AutoField(primary_key=True)
    classID = models.CharField(max_length=40)
    sessionID = models.IntegerField()
    userID = models.CharField(max_length=40)

    def __str__(self):
        return "AID = {} class id = {} session = {} | user = {} |".format(self.ID, self.classID, self.sessionID, self.userID)


class Class(models.Model):
    superUserID = models.IntegerField()
    ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    hwID = models.IntegerField()

    def __str__(self):
        return "super user = {} id = {} name = {} desc = {} hwID = {}".format(self.superUserID, self.ID, self.name, self.description, self.hwID)

class Member(models.Model):
    ID = models.AutoField(primary_key=True)
    classID = models.CharField(max_length=40)
    userID = models.CharField(max_length=40)

    def __str__(self):
        return "ID = {} class id = {} | user = {} |".format(self.ID, self.classID, self.userID)

class Session(models.Model):
    ID = models.IntegerField(primary_key=True)
    classID = models.CharField(max_length=40)
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return "ID = {} topic = {} desc = {} from {} to {}".format(self.ID, self.topic, self.description, self.start, self.end)


