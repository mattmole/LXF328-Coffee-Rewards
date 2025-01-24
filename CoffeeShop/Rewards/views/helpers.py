from Rewards.models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile
from django.template.defaulttags import register

@register.filter
def get_range(value):
    print(value)
    return range(value)


def hasAccountPermission(coffeeShop = None, account = None, user=None):
    if user!= None and user.is_superuser:
        return(True)
    
    userProfile = UserProfile.objects.get(user=user)
    accessibleCoffeeShops = CoffeeShop.objects.filter(users = userProfile)
    
    status = None
    if coffeeShop != None and account == None and user != None:
        if coffeeShop in accessibleCoffeeShops:
            status = True
        else:
            status = False
    elif account != None and coffeeShop == None and user != None:

        accountCoffeeShop = account.coffeeShop

        if accountCoffeeShop in accessibleCoffeeShops:
            status = True
        else:
            status = False
    else:
        print("Please only specify one of coffeeShop or account")
        print("The user argument is mandatory")
    print(status)
    return status