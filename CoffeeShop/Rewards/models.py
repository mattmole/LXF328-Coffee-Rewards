from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from Accounts.models import UserProfile

# Create your models here. 

class UserPermission(models.Model):
    permissionChoices = [
        ["admin", "Admin Access"],
        ["write","Write Access"],
        ["read","Read Only Access"]
        ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    permissions = models.CharField(max_length=30, help_text="Enter the permissions you want the user to have for this coffee shop", choices=permissionChoices)

    def __str__(self):
        return f"{self.user}" 
    
class CoffeeShop(models.Model):
    name = models.CharField(max_length=30, help_text="Name of the coffee shop")
    users = models.ManyToManyField(UserPermission, related_name="userPermissions")
    address = models.CharField(max_length=30, help_text="Name of the coffee shop")
    postcode = models.CharField(max_length=30, help_text="Name of the coffee shop")
    disabled = models.BooleanField(verbose_name="Account Disabled", default=False)

    def __str__(self):
        return f"{self.name} - {self.postcode}"


class Account(models.Model):
    coffeeShop = models.ForeignKey(CoffeeShop, on_delete=models.CASCADE)
    accountCode = models.CharField(verbose_name="Account Code", max_length=30, unique=True, default="")
    dateTimeCreated = models.DateTimeField(verbose_name="Date / Time Created", default=timezone.now)
    currentPoints = models.BigIntegerField(verbose_name="Current Points", default=0)
    totalPoints = models.BigIntegerField(verbose_name="Total Points Collected", default=0)
    availableRewards = models.BigIntegerField(verbose_name="Available Rewards", default=0)
    rewardsUsed = models.BigIntegerField(verbose_name="Rewards Used", default=0)
    lastModified = models.DateTimeField(verbose_name="Last Modified", editable=False)
    disabled = models.BooleanField(verbose_name="Account Disabled", default=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        #if not self.id:
        #    self.created = datetime.now()
        self.lastModified = timezone.now()
        return super(Account, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.accountCode}"

class AccountOperation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    dateTimeOfOperation = models.DateTimeField(verbose_name="Date / Time of Operation", default=datetime.now)
    operation = models.CharField(max_length=30, verbose_name="Operation")
    pointsChange = models.BigIntegerField(verbose_name="Points Change", default=0)

    def __str__(self):
        return f"{self.account} - {self.dateTimeOfOperation} - {self.operation} - {self.pointsChange}"

class AccountCodeBuilder(models.Model):
    word = models.CharField(max_length=30, unique=True, help_text="Add a word")

    def __str__(self):
        return f"{self.word}"