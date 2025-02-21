from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from Accounts.models import UserProfile

def writeAuditEntry(auditType, auditMessage, modelName, operationName, url="", user="", requestMethod=""):
    AuditEntries.objects.create(auditType = auditType, auditMessage=auditMessage, modelName=modelName, operationName=operationName, url=url, user=user, requestMethod=requestMethod)

# Create your models here. 

class AuditEntries(models.Model):
    auditType = models.CharField(max_length=30, help_text="Type of audit", blank=True)
    auditMessage = models.CharField(max_length=30, help_text="Message", blank=True)
    modelName = models.CharField(max_length=30, help_text="Model", blank=True)
    operationName = models.CharField(max_length=30, help_text="Operation Name", blank=True)
    url = models.CharField(max_length=100, help_text="Call URL", blank=True)
    user = models.CharField(max_length=100, help_text="User", blank=True)
    requestMethod = models.CharField(max_length=30, help_text="Request Method", blank=True)
    extraInfo = models.TextField(help_text="Extra information")

    dateTime = models.DateTimeField(help_text = "Timestamp of operation")
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.dateTime = timezone.now()
       
        return super(AuditEntries, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Audit Entries"
        verbose_name_plural = "Audit Entries"

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

    def save(self, url="", user="", requestMethod="", extraInfo="", *args, **kwargs):

        if not self.id:
            writeAuditEntry("ObjectCreated", "Created instance of a model", "CoffeeShop", f"{self.coffeeShop.id} - {self.coffeeShop.name}", url, user, requestMethod, extraInfo)

        writeAuditEntry("ObjectSaved", "Saved instance of a model", "AccountOperation", f"{self.coffeeShop.id} - {self.coffeeShop.name}", url, user, requestMethod, extraInfo)
       
        return super(CoffeeShop, self).save(*args, **kwargs)
    
    def delete(self, url="", user="", requestMethod="", extraInfo="", *args, **kwargs):
        parentSave = super(CoffeeShop, self).delete(*args, **kwargs)
        if parentSave:
            writeAuditEntry("ObjectDeleted", "Deleted instance of a model", "AccountOperation", f"{self.coffeeShop.id} - {self.coffeeShop.name}", url, user, requestMethod, extraInfo)

        return parentSave



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

    def save(self, url="", user="", requestMethod="", extraInfo="", *args, **kwargs):
        ''' On save, update timestamps '''
        self.lastModified = timezone.now()

        if not self.id:
            writeAuditEntry("ObjectCreated", "Created instance of a model", "Account", self.accountCode, url, user, requestMethod, extraInfo)

        writeAuditEntry("ObjectSaved", "Saved instance of a model", "Account", self.accountCode, url, user, requestMethod)
       
        return super(Account, self).save(*args, **kwargs)
    
    def delete(self, url="", user="", requestMethod="", extraInfo="", *args, **kwargs):
        parentSave = super(Account, self).delete(*args, **kwargs)
        if parentSave:
            writeAuditEntry("ObjectDeleted", "Deleted instance of a model", "Account", self.accountCode, url, user, requestMethod, extraInfo)

        return parentSave


    def __str__(self):
        return f"{self.accountCode}"

class AccountOperation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    dateTimeOfOperation = models.DateTimeField(verbose_name="Date / Time of Operation", default=datetime.now)
    operation = models.CharField(max_length=30, verbose_name="Operation")
    pointsChange = models.BigIntegerField(verbose_name="Points Change", default=0)

    def __str__(self):
        return f"{self.account} - {self.dateTimeOfOperation} - {self.operation} - {self.pointsChange}"

    def save(self, url="", user="", requestMethod="", extraInfo="", *args, **kwargs):

        if not self.id:
            writeAuditEntry("ObjectCreated", "Created instance of a model", "AccountOperation", self.account.accountCode, url, user, requestMethod, extraInfo)

        writeAuditEntry("ObjectSaved", "Saved instance of a model", "AccountOperation", self.account.accountCode, url, user, requestMethod, extraInfo)
       
        return super(AccountOperation, self).save(*args, **kwargs)
    
    def delete(self, url="", user="", requestMethod="", extraInfo="", *args, **kwargs):
        parentSave = super(AccountOperation, self).delete(*args, **kwargs)
        if parentSave:
            writeAuditEntry("ObjectDeleted", "Deleted instance of a model", "AccountOperation", self.account.accountCode, url, user, requestMethod, extraInfo)

        return parentSave

class AccountCodeBuilder(models.Model):
    word = models.CharField(max_length=30, unique=True, help_text="Add a word")

    def __str__(self):
        return f"{self.word}"