from django.urls import path
from . import views

urlpatterns = [
    path('coffeeShops', views.coffeeShops.listCoffeeShops, name='listCoffeeShops'),
    path('coffeeShops/', views.coffeeShops.listCoffeeShops, name='listCoffeeShops'),    
    path('accounts', views.accounts.listAccounts, name='listAccounts'),
    path('accounts/', views.accounts.listAccounts, name='listAccounts'),
    path('coffeeShop/<int:coffeeShopId>', views.accounts.listCoffeeShopAccounts, name='listCoffeeShopAccounts'),
    path('points/<str:accountId>', views.accounts.pointsEntry, name='pointsEntry'),
    path('deleteAccount/<str:accountId>', views.accounts.deleteAccount, name='deleteAccount'),
    path('timeline/<str:accountId>', views.accounts.timelineView, name='timelineView'),
    path('createAccount/<int:coffeeShopId>', views.accounts.createAccount, name='createAccount'),
    path('pointsBalanceUpdate', views.accounts.pointsBalanceUpdate, name='pointsBalanceUpdate'),
]
