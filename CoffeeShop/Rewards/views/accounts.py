from django.http import HttpResponseRedirect
from django.shortcuts import render
from rich import print
import math
import random
from .helpers import *

from Rewards.models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile

# Generate new account code
def genNewAccountCode():
    accounts = Account.objects.all()
    accountCodeBuilders = AccountCodeBuilder.objects.all()
    newAccountCode = ""
    if len(accountCodeBuilders) > 0:
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
    else:
        import uuid
        newAccountCode = str(uuid.uuid4())
    return newAccountCode

def listAccounts(request):
    loggedInUser = request.user

    if loggedInUser.is_anonymous:
        print("You must be logged in!")
        return render(request, "error.html", {"error": "You must be logged in!"})
    else:
        loggedInUserProfile = UserProfile.objects.get(user = loggedInUser)
        
        if loggedInUser.is_superuser:
            # Find the Coffee Shops the user can access
            availableCoffeeShops = CoffeeShop.objects.all()
        else:
            # Find the Coffee Shops the user can access
            availableCoffeeShops = CoffeeShop.objects.filter(users = loggedInUserProfile)

    availableAccounts = {}

    for coffeeShop in availableCoffeeShops:
        accounts = Account.objects.filter(coffeeShop = coffeeShop)
        availableAccounts[coffeeShop.id] = accounts

    return render(request, "accounts.html", {"availableAccounts": availableAccounts})

def listCoffeeShopAccounts(request, coffeeShopId):
    loggedInUser = request.user

    if loggedInUser.is_anonymous:
        print("You must be logged in!")
        return render(request, "error.html", {"error": "You must be logged in!"})

    loggedInUserProfile = UserProfile.objects.get(user = loggedInUser)
        
    coffeeShop = CoffeeShop.objects.get(id = coffeeShopId)

    if not loggedInUser.is_superuser:

        # Grab the user permission object for the logged in user
        userPermission = coffeeShop.users.filter(user = loggedInUserProfile)
        if len(userPermission) == 1:
            userPermission = userPermission[0]
        elif len(userPermission) == 0:

            #Does the logged in user have permissions to view this page?
            if hasCoffeeShopPermission(userProfile = loggedInUserProfile, coffeeShop=coffeeShop) == False:
                return render(request, "error.html", {"error": "You do not have permission to view this page!"})

    else:
        userPermission = None

    availableAccounts = Account.objects.filter(coffeeShop__id = coffeeShopId)

    userIsSuperAdmin = hasSuperAdmin(loggedInUser)

    newAccountCode = genNewAccountCode()

    # Generate QR Codes
    qrCodeDict = {}
    for account in availableAccounts:
        if account.accountCode not in qrCodeDict:
            qrCodeDict[account.accountCode] = generateQrCode(account.accountCode)

    return render(request, "coffeeShopAccounts.html", {"coffeeShopId": coffeeShopId, "availableAccounts": availableAccounts, "newAccountCode":newAccountCode, "userPermission": userPermission, "loggedInUser": loggedInUser, "userIsSuperAdmin":userIsSuperAdmin, "qrCodes": qrCodeDict})


def pointsEntry(request,accountId):
    loggedInUser = request.user
    if accountId == "":
        return render(request, "error.html", {"error": "No accountId sent!"})

    account = Account.objects.get(accountCode = accountId)

    loggedInUserProfile = UserProfile.objects.get(user = loggedInUser)
        
    coffeeShop = CoffeeShop.objects.get(account = account)

    userIsSuperAdmin = hasSuperAdmin(loggedInUser)


    if not loggedInUser.is_superuser:

        # Grab the user permission object for the logged in user
        userPermission = coffeeShop.users.filter(user = loggedInUserProfile)
        if len(userPermission) == 1:
            userPermission = userPermission[0]
        elif len(userPermission) == 0:

            #Does the logged in user have permissions to view this page?
            if hasCoffeeShopPermission(userProfile = loggedInUserProfile, coffeeShop=coffeeShop) == False:
                return render(request, "error.html", {"error": "You do not have permission to view this page!"})

    else:
        userPermission = None

    hasPermission = hasCoffeeShopPermission(account=account, userProfile=UserProfile.objects.get(user = loggedInUser))

    # Generate QR Code
    qrCode = generateQrCode(account.accountCode)

    if hasPermission:
        return render(request, "points.html", {"account": account, "userPermission": userPermission, "loggedInUser": loggedInUser, "userIsSuperAdmin":userIsSuperAdmin, "qrCode": qrCode})
    else:
        return render(request, "error.html", {"error": "You do not have permissions to view this page!"})
    
def pointsBalanceUpdate(request):
    pointsToAdd = int(request.POST.get('addPoints'))
    rewardsToUse = int(request.POST.get('useRewards'))
    accountId = request.POST.get('accountId')
    loggedInUser = request.user

    account = Account.objects.get(accountCode = accountId)
    linkedCoffeeShop = CoffeeShop.objects.get(account = account)

    hasPermission = hasCoffeeShopPermission(account=account, userProfile=UserProfile.objects.get(user = loggedInUser))

    if hasPermission:

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
            return render(request, "success.html", {"message": "Points have been added and / or rewards have been used!", "pointsAdded": pointsToAdd, "rewardsUsed": rewardsToUse, "redirectUrl": f"/rewards/coffeeShop/{linkedCoffeeShop.id}"})
    else:
        return render(request, "error.html", {"error": "You do not have permissions to view this page!"})

    print(account.currentPoints, account.availableRewards, account.totalPoints, account.rewardsUsed)

def timelineView(request, accountId):
    if accountId == "":
        return render(request, "error.html", {"error": "No accountId sent!"})
    loggedInUser = request.user
    account = Account.objects.get(accountCode = accountId)

    hasPermission = hasCoffeeShopPermission(account=account, userProfile=UserProfile.objects.get(user = loggedInUser))

    if hasPermission:
        accountOperations = AccountOperation.objects.filter(account = account).order_by("-dateTimeOfOperation")
        return render(request, "timeline.html", {"accountOperations": accountOperations, "account": account})
    else:
        return render(request, "error.html", {"error": "You do not have permissions to view this page!"})

def createAccount(request,coffeeShopId):
    newAccountCode = request.POST.get('newAccountCode')
    initialPoints = int(request.POST.get('initialPoints'))
    initialRewards = int(request.POST.get('initialRewards'))

    print(newAccountCode, initialPoints, initialRewards)

    newAccount = Account()
    newAccount.coffeeShop = CoffeeShop.objects.get(id = coffeeShopId)
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
        newAccountCode = genNewAccountCode()

        return render(request, "accounts.html", {"accounts": accounts, "newAccountCode":newAccountCode})
    
def deleteAccount(request, accountId):

    loggedInUser = request.user
    account = Account.objects.get(accountCode = accountId)
    hasPermission = hasCoffeeShopPermission(account=account, userProfile=UserProfile.objects.get(user = loggedInUser))

    if hasPermission:
        linkedCoffeeShop = CoffeeShop.objects.get(account = account)
        account.delete()
        return render(request, "accountDeleted.html", {"message": f"Successfully deleted: {account.accountCode} and the corresponding history","redirectUrl": f"/rewards/coffeeShop/{linkedCoffeeShop.id}"})
    else:
        return render(request, "error.html", {"error": "You do not have permissions to view this page!"})
