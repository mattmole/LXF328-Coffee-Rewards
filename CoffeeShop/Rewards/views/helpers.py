from Rewards.models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile
from django.template.defaulttags import register

@register.filter
def get_range(value):
    print(value)
    return range(value)


def hasCoffeeShopPermission(coffeeShop = None, account = None, userProfile=None):
    if userProfile != None and userProfile.user.is_superuser:
        return(True)
    
    accessibleCoffeeShops = CoffeeShop.objects.filter(users__user = userProfile)
    
    status = None
    if coffeeShop != None and account == None and userProfile!= None:
        if coffeeShop in accessibleCoffeeShops:
            status = True
        else:
            status = False
    elif account != None and coffeeShop == None and userProfile != None:

        accountCoffeeShop = account.coffeeShop

        if accountCoffeeShop in accessibleCoffeeShops:
            status = True
        else:
            status = False
    else:
        print("Please only specify one of coffeeShop or account")
        print("The user argument is mandatory")
    return status

def hasSuperAdmin(user):
    if user != None and user.is_superuser:
        return(True)
    else:
        return(False)

def userPermissions(userProfile=None, coffeeShop=None):
    superAdmin = False
    if userProfile != None and userProfile.user.is_superuser:
        return(True)