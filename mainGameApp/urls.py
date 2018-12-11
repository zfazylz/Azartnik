from django.urls import path

from .views import *

urlpatterns = [
    path('', homeView, name='home'),
    path('game/', game, name='game'),
    path('makeBet/', makeBet, name='makeBet'),
    path('closeBet/', closeBet, name='closeBet'),
    path('fillCash/', fillCashView, name='fillCash'),
    path('withdrawCash/', withdrawCashView, name='withdrawCash'),
    path('betHistory/', betHistory, name='betHistory'),
]
