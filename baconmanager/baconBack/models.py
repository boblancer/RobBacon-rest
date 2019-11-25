from django.db import models

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=50)
    lineID = models.CharField(max_length=50)

    def __str__(self):
        return "{} {}| {} |".format(self.firstName, self.lastName, self.lineID)


