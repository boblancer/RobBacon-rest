from django.db import models

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=50)
    lineID = models.CharField(max_length=50)

    def __str__(self):
        return "{} {} | {} |".format(self.firstName, self.lastName, self.lineID)

class Attendance(models.Model):
    classID = models.IntegerField()
    sessionID = models.IntegerField()
    userID = models.IntegerField()

    def __str__(self):
        return "class id = {} session = {} | user = {} |".format(self.classID, self.sessionID, self.userID)


class Class(models.Model):
    superUserID = models.IntegerField()
    ID = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    hwID = models.IntegerField()

    def __str__(self):
        return "super user = {} id = {} name = {} desc = {} hwID = {}".format(self.superUserID, self.ID, self.name, self.description, self.hwID)

class Member(models.Model):
    classID = models.IntegerField()
    userID = models.IntegerField()

    def __str__(self):
        return "class id = {} | user = {} |".format(self.classID, self.userID)

class Session(models.Model):
    ID = models.IntegerField()
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return "ID = {} topic = {} desc = {} from {} to {}".format(self.ID, self.topic, self.description, self.start, self.end)


