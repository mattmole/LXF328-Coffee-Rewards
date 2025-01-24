# Register your models here.
from django.contrib import admin
from .models import Account, AccountOperation, AccountCodeBuilder, CoffeeShop, UserProfile

class AccountAdmin(admin.ModelAdmin):
    list_display = ('accountCode', 'dateTimeCreated', 'currentPoints', 'totalPoints', 'availableRewards', 'rewardsUsed')

class AccountOperationAdmin(admin.ModelAdmin):
    list_display = ('account', 'dateTimeOfOperation', 'operation', 'pointsChange')

class AccountCodeBuilderAdmin(admin.ModelAdmin):
    list_display = ('word',)

class CoffeeShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'postcode')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountOperation, AccountOperationAdmin)
admin.site.register(AccountCodeBuilder,AccountCodeBuilderAdmin)
admin.site.register(CoffeeShop,CoffeeShopAdmin)
admin.site.register(UserProfile,UserProfileAdmin)