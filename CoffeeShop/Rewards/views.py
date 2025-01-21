from django.http import HttpResponseRedirect
from django.shortcuts import render
from rich import print
import math
import random

from .forms import PointsForm
from .models import Account, AccountOperation, AccountCodeBuilder

from django.template.defaulttags import register

@register.filter
def get_range(value):
    print(value)
    return range(value)

# Generate new account code
def genNewAccountCode(accounts):
    accountCodeBuilders = AccountCodeBuilder.objects.all()

    newAccountCode = ""
    genNewCode = True
    maxCount = 10
    while genNewCode:
        newAccountCode = f"{random.choice(accountCodeBuilders)}-{random.choice(accountCodeBuilders)}-{random.choice(accountCodeBuilders)}"
        accountsWithNewAccountCode = accounts.filter(accountCode = newAccountCode)
        print(maxCount)
        if len(accountsWithNewAccountCode) == 0 or maxCount == 0:
            genNewCode = False
            if maxCount == 0:
                newAccountCode = "ERROR"
        maxCount -= 1
    return newAccountCode

def listAccounts(request):
    accounts = Account.objects.all()

    newAccountCode = genNewAccountCode(accounts)

    return render(request, "accounts.html", {"accounts": accounts, "newAccountCode":newAccountCode})

def pointsEntry(request,accountId):
    if accountId == "":
        return render(request, "error.html", {"error": "No accountId sent!"})

    account = Account.objects.get(accountCode = accountId)

    return render(request, "points.html", {"account": account})


def pointsBalanceUpdate(request):
    pointsToAdd = int(request.POST.get('addPoints'))
    rewardsToUse = int(request.POST.get('useRewards'))
    accountId = request.POST.get('accountId')

    account = Account.objects.get(accountCode = accountId)

    # Add the reward points
    if pointsToAdd > 0:
        if pointsToAdd <= 5:
            rewardsToAdd = math.floor((account.currentPoints + pointsToAdd)/10)
            account.currentPoints = account.currentPoints + pointsToAdd - (10 * rewardsToAdd)
            account.availableRewards += rewardsToAdd
            account.totalPoints += pointsToAdd
            accountOperation = AccountOperation()
            accountOperation.account = account
            accountOperation.pointsChange=pointsToAdd
            accountOperation.operation="PointsAdded"
            accountOperation.save()

            if rewardsToAdd > 0:
                accountOperation = AccountOperation()
                accountOperation.account = account
                accountOperation.pointsChange=rewardsToAdd
                accountOperation.operation="RewardsAdded"
                accountOperation.save()

        else:
            return render(request, "error.html", {"error": "You cannot add this many points!"})
    # Remove the rewards
    if rewardsToUse > 0:
        if account.availableRewards >= rewardsToUse:
            account.availableRewards -= rewardsToUse
            account.rewardsUsed += 1
            accountOperation = AccountOperation()
            accountOperation.account = account
            accountOperation.pointsChange=rewardsToUse
            accountOperation.operation="RewardsUsed"
            accountOperation.save()
        else:
            return render(request, "error.html", {"error": "You don't have enough rewards!"})
    
    if rewardsToUse > 0 or pointsToAdd > 0:   
        account.save()
        return render(request, "success.html", {"message": "Points have been added and / or rewards have been used!", "pointsAdded": pointsToAdd, "rewardsUsed": rewardsToUse })


    print(account.currentPoints, account.availableRewards, account.totalPoints, account.rewardsUsed)

def timelineView(request, accountId):
    if accountId == "":
        return render(request, "error.html", {"error": "No accountId sent!"})
    account = Account.objects.get(accountCode = accountId)
    accountOperations = AccountOperation.objects.filter(account = account).order_by("-dateTimeOfOperation")
    return render(request, "timeline.html", {"accountOperations": accountOperations, "account": account})

def createAccount(request):
    newAccountCode = request.POST.get('newAccountCode')
    initialPoints = int(request.POST.get('initialPoints'))
    initialRewards = int(request.POST.get('initialRewards'))

    newAccount = Account()
    newAccount.accountCode = newAccountCode
    if initialPoints > 0 and initialPoints <= 5:
        newAccount.currentPoints = initialPoints
        newAccount.totalPoints = initialPoints
    if initialRewards > 0 and initialRewards <= 5:
        newAccount.availableRewards = initialRewards
    try:
        newAccount.save()
    except:
        print("Error")
    else:
        if initialPoints > 0:
            pointsOperation = AccountOperation()
            pointsOperation.account = newAccount
            pointsOperation.pointsChange = initialPoints
            pointsOperation.operation = "InitialPoints"
            pointsOperation.save()
        if initialRewards > 0:
            rewardsOperation = AccountOperation()
            rewardsOperation.account = newAccount
            rewardsOperation.pointsChange = initialRewards
            rewardsOperation.operation = "InitialRewards"
            rewardsOperation.save()
    finally:
        accounts = Account.objects.all()
        newAccountCode = genNewAccountCode(accounts)

        return render(request, "accounts.html", {"accounts": accounts, "newAccountCode":newAccountCode})
