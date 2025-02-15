from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count,Sum
from rich import print
import math
import random

from Rewards.models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile

def listCoffeeShops(request):
    loggedInUser = request.user

    if loggedInUser.is_anonymous:
        print("You must be logged in!")
        return render(request, "error.html", {"error": "You must be logged in!"})
    else:
        loggedInUserProfile = UserProfile.objects.get(user = loggedInUser)
        
        if loggedInUser.is_superuser:
            # Find the Coffee Shops the user can access
            availableCoffeeShops = CoffeeShop.objects.all().annotate(accountsCount=Count('account'),currentPoints=Sum('account__currentPoints'),availableRewards=Sum('account__availableRewards'))
        else:
            # Find the Coffee Shops the user can access
            availableCoffeeShops = CoffeeShop.objects.filter(users__user = loggedInUserProfile).annotate(accountsCount=Count('account'),currentPoints=Sum('account__currentPoints'),availableRewards=Sum('account__availableRewards'))


    return render(request, "coffeeShops.html", {"availableCoffeeShops": availableCoffeeShops})