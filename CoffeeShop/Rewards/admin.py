# Register your models here.
from django.contrib import admin
from .models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile, UserPermission, AuditEntries

class AccountAdmin(admin.ModelAdmin):
    list_display = ('accountCode', 'dateTimeCreated', 'currentPoints', 'totalPoints', 'availableRewards', 'rewardsUsed')

class AccountOperationAdmin(admin.ModelAdmin):
    list_display = ('account', 'dateTimeOfOperation', 'operation', 'pointsChange')

class AccountCodeBuilderAdmin(admin.ModelAdmin):
    list_display = ('word',)
    
class CoffeeShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'postcode')

class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permissions')

class AuditEntriesAdmin(admin.ModelAdmin):
    list_display = ('auditType', 'auditMessage', 'modelName', 'operationName', 'dateTime', 'user', 'requestMethod', 'url')

admin.site.register(UserPermission,UserPermissionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(AccountOperation, AccountOperationAdmin)
#admin.site.register(AccountCodeBuilder,AccountCodeBuilderAdmin)
admin.site.register(CoffeeShop,CoffeeShopAdmin)
admin.site.register(AuditEntries,AuditEntriesAdmin)

admin.site.site_header = "Coffee Shop Administration"
admin.site.site_title = "Coffee Shop Administration"