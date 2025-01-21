# Register your models here.
from django.contrib import admin
from .models import Account, AccountOperation, AccountCodeBuilder

class AccountAdmin(admin.ModelAdmin):
    list_display = ('accountCode', 'dateTimeCreated', 'currentPoints', 'totalPoints', 'availableRewards', 'rewardsUsed')

class AccountOperationAdmin(admin.ModelAdmin):
    list_display = ('account__accountCode', 'dateTimeOfOperation', 'operation', 'pointsChange')

class AccountCodeBuilderAdmin(admin.ModelAdmin):
    list_display = ('word',)

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountOperation, AccountOperationAdmin)
admin.site.register(AccountCodeBuilder,AccountCodeBuilderAdmin)