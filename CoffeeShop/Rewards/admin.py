# # Register your models here.
# from django.contrib import admin
# from .models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile, UserPermission, AuditEntries

# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('coffeeShop', 'accountCode', 'dateTimeCreated', 'currentPoints', 'totalPoints', 'availableRewards', 'rewardsUsed', 'disabled')

# class AccountOperationAdmin(admin.ModelAdmin):
#     list_display = ('account', 'dateTimeOfOperation', 'operation', 'pointsChange')

# class AccountCodeBuilderAdmin(admin.ModelAdmin):
#     list_display = ('word',)
    
# class CoffeeShopAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address', 'postcode')

# class UserPermissionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'permissions')

# class AuditEntriesAdmin(admin.ModelAdmin):
#     list_display = ('auditType', 'auditMessage', 'modelName', 'operationName', 'dateTime', 'user', 'requestMethod', 'url')

# admin.site.register(UserPermission,UserPermissionAdmin)
# admin.site.register(Account, AccountAdmin)
# admin.site.register(AccountOperation, AccountOperationAdmin)
# #admin.site.register(AccountCodeBuilder,AccountCodeBuilderAdmin)
# admin.site.register(CoffeeShop,CoffeeShopAdmin)
# admin.site.register(AuditEntries,AuditEntriesAdmin)

# admin.site.site_header = "Coffee Shop Administration"
# admin.site.site_title = "Coffee Shop Administration"



from django.contrib import admin

from .models import AuditEntries, UserPermission, CoffeeShop, Account, AccountOperation, AccountCodeBuilder


@admin.register(AuditEntries)
class AuditEntriesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'auditType',
        'auditMessage',
        'modelName',
        'operationName',
        'url',
        'user',
        'requestMethod',
        'extraInfo',
        'dateTime',
    )
    list_filter = ('dateTime',)


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'permissions')
    list_filter = ('user',)


@admin.register(CoffeeShop)
class CoffeeShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'postcode', 'disabled')
    list_filter = ('disabled',)
    raw_id_fields = ('users',)
    search_fields = ('name',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'coffeeShop',
        'accountCode',
        'dateTimeCreated',
        'currentPoints',
        'totalPoints',
        'availableRewards',
        'rewardsUsed',
        'lastModified',
        'disabled',
    )
    list_filter = ('dateTimeCreated', 'lastModified', 'disabled')


@admin.register(AccountOperation)
class AccountOperationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'dateTimeOfOperation',
        'operation',
        'pointsChange',
    )
    list_filter = ('dateTimeOfOperation',)


@admin.register(AccountCodeBuilder)
class AccountCodeBuilderAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')