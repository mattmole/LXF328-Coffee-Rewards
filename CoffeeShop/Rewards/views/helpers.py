from Rewards.models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile, AuditEntries
from django.template.defaulttags import register

@register.filter
def get_range(value):
    return range(value)

@register.filter(name='addClass')
def addClass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addId')
def addId(value, arg):
    return value.as_widget(attrs={'id': arg})

@register.filter(name='addIdAndClass')
def addIdAndClass(value, args):
    idArg, classArg = args.split(",")
    return value.as_widget(attrs={'id': idArg, 'class': classArg})

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
    
def generateQrCode(qrCodeText):
    import segno
    from io import BytesIO
    from base64 import b64encode

    qr = segno.make(qrCodeText, error='h')

    buffer = BytesIO()
    img = qr.to_pil(scale=5)
    img.save(buffer,"png")

    qrCode = 'data: image/png;base64, '+b64encode(buffer.getvalue()).decode('utf-8')
    return qrCode

def convertDictToFormattedJson(inputDict):
    from json import dumps
    extraInfo = dumps(inputDict, sort_keys=True, indent=2, separators=(',', ': '))
    return extraInfo