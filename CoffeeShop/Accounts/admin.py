# Register your models here.
from django.contrib import admin
from .models import UserProfile, UserPreferences

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferenceType', 'preferenceValue')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserPreferences,UserPreferencesAdmin)
