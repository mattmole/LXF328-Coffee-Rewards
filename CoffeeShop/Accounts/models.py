from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"    
    
class UserPreferences(models.Model):
    choices = (("d", "Drink"),("f", "Food"))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    preferenceType = models.CharField(
        choices=choices,
        max_length=1)
    preferenceValue = models.CharField(max_length=1000)