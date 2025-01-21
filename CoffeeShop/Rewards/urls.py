from django.urls import path
from . import views

urlpatterns = [
    path('points', views.listAccounts, name='listAccounts'),
    path('points/', views.listAccounts, name='listAccounts'),
    path('points/<str:accountId>', views.pointsEntry, name='pointsEntry'),
    path('timeline/<str:accountId>', views.timelineView, name='timelineView'),
    path('createAccount', views.createAccount, name='createAccount'),
    path('pointsBalanceUpdate', views.pointsBalanceUpdate, name='pointsBalanceUpdate'),
]
