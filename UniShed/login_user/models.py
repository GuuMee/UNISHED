from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(model.Model): #this class inherit from models.Model

    user = models.OneToOneField(User) #that's extending the class oneToOne -relationship, field with the user itself
    #the reason for that is because this is a Model class to add an additional information that the defaultuser doesn't have

    def __str__(self):
        return self.user.username